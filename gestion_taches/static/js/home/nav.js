document.addEventListener('DOMContentLoaded', function () {
function setupActiveNavigation() {
  // Récupérer tous les liens de navigation
  const navLinks = document.querySelectorAll('nav-link');

  // Obtenir l'URL actuelle
  const currentPath = window.location.pathname;

  navLinks.forEach(link => {
    // Vérifie si le href du lien correspond à la page actuelle
    if (link.getAttribute('href') === currentPath) {
      link.classList.add('active'); // ajoute une classe active
    } else {
      link.classList.remove('active'); // retire si ce n'est pas la page actuelle
    }
  });
}

})
