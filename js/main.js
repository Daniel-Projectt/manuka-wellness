// MANUKA — interacciones

(function () {
  "use strict";

  // Nav sólida al hacer scroll
  const nav = document.getElementById("main-nav");
  if (nav) {
    const onScroll = () => nav.classList.toggle("is-solid", window.scrollY > 40);
    window.addEventListener("scroll", onScroll, { passive: true });
    onScroll();
  }

  // Menú móvil
  const hamburger = document.getElementById("hamburger");
  const overlay = document.getElementById("nav-overlay");
  const overlayClose = document.getElementById("overlay-close");

  if (hamburger && overlay) {
    const openMenu = () => {
      overlay.classList.add("is-open");
      hamburger.setAttribute("aria-expanded", "true");
      document.body.style.overflow = "hidden";
    };
    const closeMenu = () => {
      overlay.classList.remove("is-open");
      hamburger.setAttribute("aria-expanded", "false");
      document.body.style.overflow = "";
    };

    hamburger.addEventListener("click", openMenu);
    if (overlayClose) overlayClose.addEventListener("click", closeMenu);
    overlay.querySelectorAll("a").forEach((link) => link.addEventListener("click", closeMenu));
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && overlay.classList.contains("is-open")) closeMenu();
    });
  }

  // Avisa al respaldo del <head> que el revelado sí va a ocurrir
  window.__manukaReveal = true;

  // Revelado al hacer scroll
  const reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12 }
    );
    reveals.forEach((el) => observer.observe(el));
  } else {
    reveals.forEach((el) => el.classList.add("is-visible"));
  }

  // CTA fija de móvil: solo cuando el hero ya quedó atrás
  const ctaFija = document.querySelector(".cta-fija");
  const hero = document.getElementById("inicio");
  if (ctaFija && hero && "IntersectionObserver" in window) {
    const heroObserver = new IntersectionObserver(
      ([entry]) => ctaFija.classList.toggle("is-shown", !entry.isIntersecting),
      { threshold: 0, rootMargin: "-40% 0px 0px 0px" }
    );
    heroObserver.observe(hero);
  }

  // Año del footer
  const year = document.getElementById("year");
  if (year) year.textContent = new Date().getFullYear();
})();
