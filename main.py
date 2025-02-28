"""
Ce fichier contient le code de l'API FastAPI qui permet de générer des titres à partir de résumés de texte.
Le modèle T5 entraîné est chargé et utilisé pour générer les titres.

Utilisation : 
- uvicorn main:app

"""

# Configuration des templates et fichiers statiques
from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import torch
from transformers import T5Tokenizer, T5ForConditionalGeneration

app = FastAPI()

# Configuration des templates et fichiers statiques
templates = Jinja2Templates(directory="assets/html") 

app.mount("/css", StaticFiles(directory="assets/css"), name="css") 
app.mount("/img", StaticFiles(directory="assets/img"), name="img") 
app.mount("/js", StaticFiles(directory="assets/js"), name="js")


# On charge ton modèle entraîné
model_save_path = "./model"  
tokenizer = T5Tokenizer.from_pretrained(model_save_path)
model = T5ForConditionalGeneration.from_pretrained(model_save_path)

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Le endpoint pour générer un titre
@app.post("/generate")
async def generate_title(request: Request, summary: str = Form(...)):
    input_ids = tokenizer.encode(summary, return_tensors="pt")

    generated_titles = set()
    
    while len(generated_titles) < 3 :  # Générer 3 titres uniques
        with torch.no_grad():
            generated_ids = model.generate(
                input_ids,
                max_length=10,
                min_length=3,
                num_beams=5,
                temperature=1.0,
                top_k=50,
                top_p=0.9,
                do_sample=True,
                early_stopping=True
            )
        title = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
        generated_titles.add(title)

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "generated_titles": list(generated_titles),
            "summary": summary
        },
    )