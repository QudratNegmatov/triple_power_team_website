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

    var testimonialGroups = document.querySelectorAll(".testimonial-slide-group");
    var testimonialDots = document.querySelectorAll(".testimonial-dot");
    if (testimonialGroups.length > 1) {
        var testimonialCurrent = 0;
        var showTestimonials = function (index) {
            testimonialCurrent = (index + testimonialGroups.length) % testimonialGroups.length;
            testimonialGroups.forEach(function (group, i) {
                group.classList.toggle("is-active", i === testimonialCurrent);
            });
            testimonialDots.forEach(function (dot, i) {
                dot.classList.toggle("is-active", i === testimonialCurrent);
            });
        };
        testimonialDots.forEach(function (dot, i) {
            dot.addEventListener("click", function () { showTestimonials(i); });
        });
        setInterval(function () { showTestimonials(testimonialCurrent + 1); }, 7000);
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
