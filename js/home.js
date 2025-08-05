document.addEventListener("DOMContentLoaded", () => {
  const menuBtn = document.getElementById('menu-toggle');
  const mobileMenu = document.getElementById('mobile-menu');
  const desktopMenu = document.getElementById('desktop-menu');

  // Detectar si es mobile
  const isMobile = () => window.matchMedia("(max-width: 768px)").matches;

  menuBtn.addEventListener('click', (e) => {
    e.stopPropagation();

    if (isMobile()) {
      // Controla SOLO el menú móvil
      mobileMenu.classList.toggle('open');
      menuBtn.classList.toggle('open');
    } else {
      // Controla SOLO el menú desktop
      desktopMenu.classList.toggle('open');
    }
  });

  // Cerrar si se hace clic fuera
  document.addEventListener('click', (e) => {
    if (isMobile()) {
      if (!mobileMenu.contains(e.target) && !menuBtn.contains(e.target)) {
        mobileMenu.classList.remove('open');
        menuBtn.classList.remove('open');
      }
    } else {
      if (!desktopMenu.contains(e.target) && !menuBtn.contains(e.target)) {
        desktopMenu.classList.remove('open');
      }
    }
  });

  // Cerrar con tecla Esc
  document.addEventListener('keydown', (e) => {
    if (e.key === "Escape") {
      mobileMenu.classList.remove('open');
      desktopMenu.classList.remove('open');
      menuBtn.classList.remove('open');
    }
  });
});