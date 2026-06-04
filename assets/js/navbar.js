/**
 * navbar.js — Shared navbar loader
 *
 * Drop a <div id="navbar-root"></div> anywhere in your <body> and this script
 * will fetch navbar.html, inject it, then mark the current page link as active.
 *
 * Usage on any page:
 *   <link rel="stylesheet" href="./assets/css/navbar.css">
 *   <div id="navbar-root"></div>
 *   <script src="./assets/js/navbar.js"></script>
 */

(function () {
    const ROOT_ID = "navbar-root";

    // ── 1. Resolve path to navbar.html relative to current page ──────────
    const scriptSrc  = document.currentScript?.src ?? "";
    const scriptDir  = scriptSrc.substring(0, scriptSrc.lastIndexOf("/assets/js/"));
    const navbarPath = scriptDir + "/navbar.html";

    // ── 2. Fetch and inject ───────────────────────────────────────────────
    fetch(navbarPath)
        .then(res => {
            if (!res.ok) throw new Error(`Failed to load navbar.html (${res.status})`);
            return res.text();
        })
        .then(html => {
            const root = document.getElementById(ROOT_ID);
            if (!root) {
                console.warn(`[navbar.js] No element with id="${ROOT_ID}" found.`);
                return;
            }

            root.outerHTML = html;

            // ── 3. Mark current page link as active ───────────────────────
            const current = window.location.pathname.split("/").pop() || "index.html";

            document.querySelectorAll(".nav-link").forEach(link => {
                const href = link.getAttribute("href") ?? "";
                const linkPage = href.split("/").pop();
                if (linkPage === current) {
                    link.classList.add("active");
                    link.setAttribute("aria-current", "page");
                }
            });
        })
        .catch(err => console.error("[navbar.js]", err));
})();
