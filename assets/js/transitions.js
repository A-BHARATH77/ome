/**
 * page-transition.js
 * Intercepts internal link clicks and runs a curtain wipe animation
 * between pages so there's no jarring hard-reload flash.
 *
 * Add to every page:
 *   <link rel="stylesheet" href="./assets/css/transitions.css">
 *   <div id="page-curtain"></div>
 *   <script src="./assets/js/transitions.js"></script>
 */

(function () {
    const CURTAIN_ID   = "page-curtain";
    const EXIT_CLASS   = "curtain-cover";
    const REVEAL_CLASS = "curtain-reveal";
    const DURATION_MS  = 600; // must match CSS transition duration

    const curtain = document.getElementById(CURTAIN_ID);
    if (!curtain) return;

    // ── On page ENTER: slide curtain away to reveal the new page ─────────
    window.addEventListener("DOMContentLoaded", () => {
        curtain.classList.add(REVEAL_CLASS);
        setTimeout(() => curtain.classList.remove(REVEAL_CLASS), DURATION_MS);
    });

    // ── On link click: cover with curtain then navigate ───────────────────
    document.addEventListener("click", e => {
        const link = e.target.closest("a[href]");
        if (!link) return;

        const href = link.getAttribute("href");

        // Only intercept same-origin internal page links (not anchors, mailto, external)
        if (
            !href ||
            href.startsWith("#") ||
            href.startsWith("mailto:") ||
            href.startsWith("tel:") ||
            href.startsWith("http") ||
            link.hasAttribute("target")
        ) return;

        e.preventDefault();

        // Slide curtain in to cover current page
        curtain.classList.add(EXIT_CLASS);

        setTimeout(() => {
            window.location.href = href;
        }, DURATION_MS);
    });
})();
