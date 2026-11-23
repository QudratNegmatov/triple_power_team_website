document.addEventListener("DOMContentLoaded", function () {
    var header = document.querySelector(".site-header");
    if (header) {
        var onScroll = function () {
            header.classList.toggle("scrolled", window.scrollY > 8);
        };
        onScroll();
        window.addEventListener("scroll", onScroll, { passive: true });
    }

    var navToggle = document.querySelector(".nav-toggle");
    if (header && navToggle) {
        navToggle.addEventListener("click", function () {
            var open = header.classList.toggle("nav-open");
            navToggle.setAttribute("aria-expanded", open ? "true" : "false");
        });
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
    var heroCopySlides = document.querySelectorAll(".hero-copy-slide");
    var heroDots = document.querySelectorAll(".hero-slider-dot");
    if (heroSlides.length > 1) {
        var heroCurrent = 0;
        var showHero = function (index) {
            heroCurrent = (index + heroSlides.length) % heroSlides.length;
            heroSlides.forEach(function (slide, i) {
                slide.classList.toggle("is-active", i === heroCurrent);
                // Videos of later slides only download when their slide is shown.
                var video = slide.querySelector("video[data-src]");
                if (video && i === heroCurrent) {
                    video.src = video.getAttribute("data-src");
                    video.removeAttribute("data-src");
                    video.play().catch(function () {});
                }
            });
            heroCopySlides.forEach(function (slide, i) {
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

    document.querySelectorAll(".gallery-slider").forEach(function (slider) {
        var slides = slider.querySelectorAll(".gallery-slide");
        var dots = slider.querySelectorAll(".gallery-dot");
        if (slides.length > 1) {
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
            dots.forEach(function (dot, i) {
                dot.addEventListener("click", function () { show(i); });
            });
            setInterval(function () { show(current + 1); }, 5000);
        }
    });
});
