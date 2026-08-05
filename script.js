/* ============================================================
   Dante — Portfolio
   Interacciones: scroll reveal + smooth nav + theme detection
   ============================================================ */

(() => {
  "use strict";

  /* ---------- Scroll reveal ---------- */
  const revealTargets = document.querySelectorAll(
    ".section-head, .bento > *, .proj, .repo, .stack-col, .tl-item, .contact-card, .hero-text > *, .hero-visual, .kpis"
  );
  revealTargets.forEach(el => el.classList.add("reveal"));

  if ("IntersectionObserver" in window) {
    const io = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            io.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
    );
    revealTargets.forEach((el) => io.observe(el));
  } else {
    revealTargets.forEach((el) => el.classList.add("is-visible"));
  }

  /* ---------- Smooth nav with header offset ---------- */
  const header = document.querySelector(".topbar");
  const headerH = () => (header ? header.offsetHeight : 0);

  document.querySelectorAll('a[href^="#"]').forEach((a) => {
    a.addEventListener("click", (e) => {
      const id = a.getAttribute("href");
      if (!id || id === "#") return;
      const target = document.querySelector(id);
      if (!target) return;
      e.preventDefault();
      const y = target.getBoundingClientRect().top + window.scrollY - headerH() - 8;
      window.scrollTo({ top: y, behavior: "smooth" });
    });
  });

  /* ---------- Active nav link on scroll ---------- */
  const navLinks = document.querySelectorAll(".nav a[href^='#']");
  const sections = Array.from(navLinks)
    .map((a) => document.querySelector(a.getAttribute("href")))
    .filter(Boolean);

  if ("IntersectionObserver" in window && sections.length) {
    const navIO = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (e.isIntersecting) {
            const id = "#" + e.target.id;
            navLinks.forEach((l) => {
              l.style.color = l.getAttribute("href") === id ? "var(--text-1)" : "";
              l.style.background = l.getAttribute("href") === id ? "var(--bg-2)" : "";
            });
          }
        });
      },
      { rootMargin: "-40% 0px -50% 0px" }
    );
    sections.forEach((s) => navIO.observe(s));
  }

  /* ---------- Topbar shadow on scroll ---------- */
  let lastY = 0;
  const onScroll = () => {
    const y = window.scrollY;
    if (header) {
      if (y > 8) {
        header.style.boxShadow = "0 6px 28px rgba(0,0,0,0.45)";
      } else {
        header.style.boxShadow = "none";
      }
    }
    lastY = y;
  };
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  /* ---------- Konami-free: simple stat counter on first view ---------- */
  const counters = document.querySelectorAll("[data-count]");
  if (counters.length && "IntersectionObserver" in window) {
    const cIO = new IntersectionObserver(
      (entries) => {
        entries.forEach((e) => {
          if (!e.isIntersecting) return;
          const el = e.target;
          const target = parseFloat(el.dataset.count);
          const suffix = el.dataset.suffix || "";
          const decimals = (el.dataset.count.split(".")[1] || "").length;
          const dur = 1100;
          const t0 = performance.now();
          const tick = (t) => {
            const p = Math.min(1, (t - t0) / dur);
            const ease = 1 - Math.pow(1 - p, 3);
            const v = target * ease;
            el.textContent = v.toFixed(decimals) + suffix;
            if (p < 1) requestAnimationFrame(tick);
          };
          requestAnimationFrame(tick);
          cIO.unobserve(el);
        });
      },
      { threshold: 0.4 }
    );
    counters.forEach((c) => cIO.observe(c));
  }
})();
