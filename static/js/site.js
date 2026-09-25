document.addEventListener("DOMContentLoaded", function () {
    var header = document.querySelector(".site-header");
    if (header) {
        var onScroll = function () {
            header.classList.toggle("scrolled", window.scrollY > 8);
        };
        onScroll();
        window.addEventListener("scroll", onScroll, { passive: true });
    }

    var revealEls = document.querySelectorAll(".reveal");
    if (revealEls.length) {
        if ("IntersectionObserver" in window) {
            var observer = new IntersectionObserver(
                function (entries) {
                    entries.forEach(function (entry) {
                        if (entry.isIntersecting) {
                            entry.target.classList.add("in-view");
                            observer.unobserve(entry.target);
                        }
                    });
                },
                { threshold: 0.15 }
            );
            revealEls.forEach(function (el) { observer.observe(el); });
        } else {
            revealEls.forEach(function (el) { el.classList.add("in-view"); });
        }
    }

    var slides = document.querySelectorAll(".testimonial-slide");
    var dots = document.querySelectorAll(".testimonial-dot");
    if (slides.length) {
        var current = 0;
        var show = function (index) {
            current = (index + slides.length) % slides.length;
            slides.forEach(function (slide, i) {
                slide.classList.toggle("is-active", i === current);
            });
            dots.forEach(function (dot, i) {
                dot.classList.toggle("is-active", i === current);
            });
        };
        var prevBtn = document.querySelector("[data-testimonial-prev]");
        var nextBtn = document.querySelector("[data-testimonial-next]");
        if (prevBtn) prevBtn.addEventListener("click", function () { show(current - 1); });
        if (nextBtn) nextBtn.addEventListener("click", function () { show(current + 1); });
        dots.forEach(function (dot, i) {
            dot.addEventListener("click", function () { show(i); });
        });
    }

    var heroSlides = document.querySelectorAll(".hero-slide");
    var heroDots = document.querySelectorAll(".hero-slider-dot");
    if (heroSlides.length > 1) {
        var heroCurrent = 0;
        var showHero = function (index) {
            heroCurrent = (index + heroSlides.length) % heroSlides.length;
            heroSlides.forEach(function (slide, i) {
                slide.classList.toggle("is-active", i === heroCurrent);
            });
            heroDots.forEach(function (dot, i) {
                dot.classList.toggle("is-active", i === heroCurrent);
            });
        };
        heroDots.forEach(function (dot, i) {
            dot.addEventListener("click", function () { showHero(i); });
        });
        setInterval(function () { showHero(heroCurrent + 1); }, 6000);
    }
});
