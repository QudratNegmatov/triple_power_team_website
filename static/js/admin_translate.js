/* "Translate" buttons on admin change forms.
 *
 * Finds every English field (name ending in "_en") that has "_uz" and "_ru"
 * siblings, sends the English text to /admin/translate/, and fills the Uzbek
 * and Russian fields with the result. Nothing is saved - the editor reviews
 * the highlighted fields and clicks Save as usual.
 */
(function () {
    "use strict";

    var config = JSON.parse(document.getElementById("admin-translate-config").textContent);
    var form = document.querySelector("#content-main form");
    if (!form) return;

    var LANGS = ["uz", "ru"];

    function editorFor(el) {
        return window.CKEDITOR && el.id && window.CKEDITOR.instances[el.id];
    }
    function getValue(el) {
        var editor = editorFor(el);
        return editor ? editor.getData() : el.value;
    }
    function setValue(el, value) {
        var editor = editorFor(el);
        if (editor) editor.setData(value);
        else el.value = value;
        var box = editor ? document.getElementById("cke_" + el.id) : el;
        if (box) box.classList.add("tr-filled");
    }

    // Groups of {key, en, uz, ru} for the translatable fields currently on the form
    // (inline rows added with "Add another" are picked up on each click).
    function collectGroups() {
        var groups = [];
        form.querySelectorAll("input[name$='_en'], textarea[name$='_en']").forEach(function (en) {
            if (en.type === "hidden" || en.name.indexOf("__prefix__") !== -1) return;
            var base = en.name.slice(0, -3);
            var uz = form.querySelector("[name='" + base + "_uz']");
            var ru = form.querySelector("[name='" + base + "_ru']");
            if (uz && ru) groups.push({ key: base, en: en, uz: uz, ru: ru });
        });
        return groups;
    }

    var groups = collectGroups();
    if (!groups.length) return;

    var bar = document.createElement("div");
    bar.className = "tr-bar";
    bar.innerHTML =
        '<strong>Auto-translate</strong> ' +
        '<span class="tr-help">Fill in English, then translate to O\'zbekcha and Русский. ' +
        "Translations are not saved until you review them and click Save.</span>" +
        '<div class="tr-actions">' +
        '<button type="button" class="button tr-empty">Translate EN → UZ, RU (empty fields)</button> ' +
        '<button type="button" class="button tr-all">Re-translate all (overwrite)</button> ' +
        '<span class="tr-status" role="status"></span>' +
        "</div>";
    form.insertBefore(bar, form.firstElementChild);

    var status = bar.querySelector(".tr-status");
    var buttons = bar.querySelectorAll("button");

    function csrfToken() {
        var input = form.querySelector("[name=csrfmiddlewaretoken]");
        return input ? input.value : "";
    }

    function run(overwrite) {
        var current = collectGroups();
        var todo = current.filter(function (g) {
            if (!getValue(g.en).trim()) return false;
            return overwrite || LANGS.some(function (l) { return !getValue(g[l]).trim(); });
        });
        if (!todo.length) {
            status.textContent = "Nothing to translate - every field with English text already has UZ and RU.";
            return;
        }
        if (overwrite && !window.confirm("Overwrite the existing Uzbek and Russian text in " + todo.length + " field(s)?")) {
            return;
        }

        var fields = todo.map(function (g) {
            var maxLength = Math.min(
                g.uz.maxLength > 0 ? g.uz.maxLength : Infinity,
                g.ru.maxLength > 0 ? g.ru.maxLength : Infinity
            );
            return {
                key: g.key,
                text: getValue(g.en),
                html: !!editorFor(g.en),
                max_length: isFinite(maxLength) ? maxLength : null,
            };
        });

        buttons.forEach(function (b) { b.disabled = true; });
        status.textContent = "Translating " + fields.length + " field(s)… this can take up to a minute.";

        fetch(config.url, {
            method: "POST",
            credentials: "same-origin",
            headers: { "Content-Type": "application/json", "X-CSRFToken": csrfToken() },
            body: JSON.stringify({ fields: fields }),
        })
            .then(function (resp) {
                return resp.json().catch(function () { return { error: "Server error (" + resp.status + ")." }; });
            })
            .then(function (data) {
                if (data.error) throw new Error(data.error);
                var filled = 0;
                todo.forEach(function (g) {
                    var t = data.translations[g.key];
                    if (!t) return;
                    LANGS.forEach(function (l) {
                        if (overwrite || !getValue(g[l]).trim()) {
                            setValue(g[l], t[l]);
                            filled++;
                        }
                    });
                });
                status.textContent = "Done: " + filled + " field(s) filled (highlighted). Review them, then click Save.";
            })
            .catch(function (err) {
                status.textContent = err.message || "Translation failed.";
            })
            .finally(function () {
                buttons.forEach(function (b) { b.disabled = false; });
            });
    }

    bar.querySelector(".tr-empty").addEventListener("click", function () { run(false); });
    bar.querySelector(".tr-all").addEventListener("click", function () { run(true); });

    var style = document.createElement("style");
    style.textContent =
        ".tr-bar{margin:0 0 20px;padding:12px 14px;border:1px solid var(--hairline-color,#ddd);" +
        "border-left:4px solid #22c55e;border-radius:4px;background:var(--darkened-bg,#f8f8f8)}" +
        ".tr-help{color:var(--body-quiet-color,#666);font-size:12px}" +
        ".tr-actions{margin-top:8px;display:flex;gap:8px;align-items:center;flex-wrap:wrap}" +
        ".tr-status{font-size:12px}" +
        ".tr-filled{outline:2px solid #facc15!important;outline-offset:1px}";
    document.head.appendChild(style);
})();
