#!/usr/bin/env python3
"""
Generate about.html from index.html by:
1. Removing the custom hero section
2. Removing framer-i2anp5 display:none style
3. Removing GSAP/counter/hero animation scripts
4. Adding history.replaceState('/about') before head.js loads
5. Removing the route-visibility script (not needed)
"""

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# ── 1. Remove the framer-i2anp5 hide style ──────────────────────────────────
content = content.replace(
    '<style>.framer-i2anp5 { display: none !important; }</style>',
    ''
)

# ── 2. Remove GSAP preload hints ─────────────────────────────────────────────
content = content.replace(
    '  <!-- Preload GSAP so it starts fetching at the earliest possible moment -->\n'
    '  <link rel="preload" href="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js" as="script">\n'
    '  <link rel="preload" href="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/Flip.min.js" as="script">\n',
    ''
)

# ── 3. Remove the entire custom hero <section> (from <section class="hero"> to </section>) ──
import re

# Remove hero section
hero_pattern = re.compile(
    r'\n\s*<section class="hero"[^>]*>.*?</section>\s*\n',
    re.DOTALL
)
content = hero_pattern.sub('\n', content)

# ── 4. Remove duplicate <div id="main"> ─────────────────────────────────────
# Keep only one, the second one
content = re.sub(
    r'<div id="main">\s*<!-- Content will be loaded here -->\s*</div>\s*\n\s*\n\s*<div id="main">\s*<!-- Content will be loaded here -->\s*</div>',
    '<div id="main">\n        <!-- Content will be loaded here -->\n    </div>',
    content
)

# ── 5. Remove GSAP script tags ───────────────────────────────────────────────
content = content.replace(
    '\n    <script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/gsap.min.js"></script>',
    ''
)
content = content.replace(
    '\n<script src="https://cdn.jsdelivr.net/npm/gsap@3.12.5/dist/Flip.min.js"></script>',
    ''
)

# ── 6. Remove our huge GSAP/animation IIFE script ───────────────────────────
# It starts with `<script>\n\n    gsap.registerPlugin(Flip);` and ends with `  </script>`
gsap_script_pattern = re.compile(
    r'<script>\s*\n\s*gsap\.registerPlugin\(Flip\);.*?</script>',
    re.DOTALL
)
content = gsap_script_pattern.sub('', content)

# ── 7. Remove route-visibility script ───────────────────────────────────────
route_vis_pattern = re.compile(
    r'<!-- Hide our custom hero when Framer routes away from home -->.*?</script>',
    re.DOTALL
)
content = route_vis_pattern.sub('', content)

# ── 8. Add history.replaceState before <script src="head.js"> ───────────────
replacestate = (
    '<script>\n'
    '    // Tell Framer router to render the /about route\n'
    '    (function() {\n'
    "        var url = location.href.replace(/about\\.html([?#].*)?$/, 'about$1');\n"
    '        history.replaceState(null, \'\', url);\n'
    '    })();\n'
    '</script>\n    '
)
content = content.replace(
    '    <script src="head.js"></script>',
    replacestate + '<script src="head.js"></script>'
)

# ── 9. Update title and meta description for about page ─────────────────────
content = content.replace(
    '<title>Slay The Strategy</title>',
    '<title>About — Slay The Strategy</title>'
)
content = content.replace(
    'content="Slay The Strategy is a refined strategy template crafted to showcase your work with clarity, structure, and intentional motion."',
    'content="About Slay The Strategy — a creative studio crafting visual narratives for brands that demand attention."'
)

# ── 10. Write out ─────────────────────────────────────────────────────────────
with open('about.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("about.html generated successfully!")
