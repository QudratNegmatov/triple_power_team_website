(function () {
    "use strict";

    // Mobile sidebar
    document.querySelectorAll("[data-sidebar-toggle]").forEach(function (btn) {
        btn.addEventListener("click", function () { document.body.classList.toggle("sidebar-open"); });
    });
    document.addEventListener("click", function (e) {
        if (document.body.classList.contains("sidebar-open") && !e.target.closest(".sidebar, [data-sidebar-toggle]")) {
            document.body.classList.remove("sidebar-open");
        }
    });

    // List filters submit on change
    document.querySelectorAll("[data-autosubmit]").forEach(function (el) {
        el.addEventListener("change", function () { el.form.submit(); });
    });

    // Language switch (EN / UZ / RU) for translated fields
    var form = document.querySelector(".edit-form[data-lang]");
    function setLang(code) {
        if (!form) return;
        form.setAttribute("data-lang", code);
        form.querySelectorAll("[data-lang-btn]").forEach(function (b) {
            b.classList.toggle("is-active", b.getAttribute("data-lang-btn") === code);
        });
        try { sessionStorage.setItem("panel-lang", code); } catch (e) {}
    }
    if (form) {
        form.querySelectorAll("[data-lang-btn]").forEach(function (b) {
            b.addEventListener("click", function () { setLang(b.getAttribute("data-lang-btn")); });
        });
        // Mark languages that have errors, and open the first one.
        var errorLangs = [];
        form.querySelectorAll(".tr-input").forEach(function (box) {
            if (box.querySelector(".err")) errorLangs.push(box.getAttribute("data-lang-input"));
        });
        errorLangs.forEach(function (code) {
            var b = form.querySelector('[data-lang-btn="' + code + '"]');
            if (b) b.classList.add("has-error");
        });
        var saved = null;
        try { saved = sessionStorage.getItem("panel-lang"); } catch (e) {}
        setLang(errorLangs[0] || saved || "en");
    }

    // Image / file inputs: show the chosen file
    function bindUpload(root) {
        root.querySelectorAll("[data-upload] input[type=file]").forEach(function (input) {
            input.addEventListener("change", function () {
                var box = input.closest("[data-upload]");
                var file = input.files && input.files[0];
                var name = box.querySelector("[data-file-name]");
                if (name) name.textContent = file ? file.name : "";
                var img = box.querySelector("[data-preview]");
                var empty = box.querySelector("[data-preview-empty]");
                if (img && file && file.type.indexOf("image/") === 0) {
                    img.src = URL.createObjectURL(file);
                    img.hidden = false;
                    if (empty) empty.hidden = true;
                }
            });
        });
    }

    // Rich text editor
    function bindEditors(root) {
        root.querySelectorAll("[data-rte]").forEach(function (box) {
            if (box.dataset.ready) return;
            box.dataset.ready = "1";
            var area = box.querySelector(".rte-area");
            var source = box.querySelector(".rte-source");
            area.innerHTML = source.value;
            var sync = function () {
                if (!box.classList.contains("is-html")) source.value = area.innerHTML.trim() === "<br>" ? "" : area.innerHTML;
            };
            area.addEventListener("input", sync);
            box.querySelectorAll("[data-cmd]").forEach(function (btn) {
                btn.addEventListener("mousedown", function (e) { e.preventDefault(); });
                btn.addEventListener("click", function () {
                    var cmd = btn.getAttribute("data-cmd");
                    var arg = btn.getAttribute("data-arg");
                    if (cmd === "createLink") {
                        arg = window.prompt("Havola manzili (https://...):", "https://");
                        if (!arg) return;
                    }
                    area.focus();
                    document.execCommand(cmd, false, arg);
                    sync();
                });
            });
            var toggle = box.querySelector("[data-html-toggle]");
            toggle.addEventListener("click", function () {
                if (box.classList.contains("is-html")) {
                    area.innerHTML = source.value;
                    box.classList.remove("is-html");
                } else {
                    sync();
                    box.classList.add("is-html");
                }
            });
            if (box.closest("form")) box.closest("form").addEventListener("submit", sync);
        });
    }

    // Inline items (gallery, systems, ...): add new / mark for delete
    document.querySelectorAll("[data-inline]").forEach(function (block) {
        var prefix = block.getAttribute("data-inline");
        var total = block.querySelector('input[name="' + prefix + '-TOTAL_FORMS"]');
        var list = block.querySelector(".inline-items");
        var tpl = block.querySelector("template[data-empty-form]");
        block.querySelector("[data-add-inline]").addEventListener("click", function () {
            var index = parseInt(total.value, 10);
            var html = tpl.innerHTML.replace(/__prefix__/g, String(index));
            var wrap = document.createElement("div");
            wrap.innerHTML = html.trim();
            var item = wrap.firstElementChild;
            list.appendChild(item);
            total.value = String(index + 1);
            bindUpload(item);
            bindEditors(item);
            var remove = item.querySelector("[data-remove-new]");
            if (remove) remove.addEventListener("click", function () {
                if (item === list.lastElementChild && parseInt(total.value, 10) === index + 1) {
                    item.remove();
                    total.value = String(index);
                    return;
                }
                // Not the last one: put its defaults back, so Django sees an
                // unchanged extra row and skips it.
                item.querySelectorAll("input, textarea, select").forEach(function (el) {
                    if (el.type === "checkbox") el.checked = el.defaultChecked;
                    else if (el.type === "file") el.value = "";
                    else if (el.tagName === "SELECT") el.selectedIndex = Math.max(0, Array.prototype.findIndex.call(el.options, function (o) { return o.defaultSelected; }));
                    else el.value = el.defaultValue;
                });
                item.hidden = true;
            });
            var first = item.querySelector("input[type=text], textarea");
            if (first) first.focus();
        });
        block.querySelectorAll(".inline-delete input[type=checkbox]").forEach(function (cb) {
            cb.addEventListener("change", function () { cb.closest(".inline-item").classList.toggle("is-deleted", cb.checked); });
        });
    });

    bindUpload(document);
    bindEditors(document);
})();
