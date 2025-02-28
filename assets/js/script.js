document.addEventListener("DOMContentLoaded", function () {
  const menuBtn = document.getElementById("menu-btn");
  const dropdownMenu = document.getElementById("dropdown-menu");

  menuBtn.addEventListener("click", function (event) {
      event.preventDefault(); // Empêche le rechargement de la page
      dropdownMenu.classList.toggle("show-menu"); // Ajoute ou enlève la classe
  });

  // Fermer le menu quand on clique ailleurs
  document.addEventListener("click", function (event) {
      if (!menuBtn.contains(event.target) && !dropdownMenu.contains(event.target)) {
          dropdownMenu.classList.remove("show-menu");
      }
  });
});

