import re

with open('/Users/apple/Desktop/ome/index.html', 'r') as f:
    html = f.read()

# 1. Remove the preloader CSS
preloader_css_pattern = r'\.preloader-overlay\s*\{.*?\.preloader-text\s*\{[^\}]*\}'
html = re.sub(preloader_css_pattern, '', html, flags=re.DOTALL)

# 2. Update .hero CSS to have sticky positioning and z-index
hero_css_pattern = r'(\.hero\s*\{.*?position:\s*)relative(.*?height:\s*100svh;)'
html = re.sub(hero_css_pattern, r'\g<1>sticky;\n      top: 0;\n      z-index: 1\g<2>', html, flags=re.DOTALL)

# 3. Add #main CSS
main_css = "\n    #main {\n      position: relative;\n      z-index: 2;\n      background-color: var(--bg);\n    }\n"
# we can just insert this before `</style>` 
# Wait, let's just replace `.hero` with `.hero` and `#main`
html = html.replace('.hero {', '#main { position: relative; z-index: 2; background-color: var(--bg); }\n\n    .hero {')

# 4. Add transform: scale(0); to .img
img_css_pattern = r'(\.images-container \.img\s*\{.*?overflow:\s*hidden;)'
html = re.sub(img_css_pattern, r'\1\n      transform: scale(0);', html, flags=re.DOTALL)

# 5. Remove the HTML for preloader
html = re.sub(r'<div class="preloader-overlay">\s*<h1 class="preloader-text">Let\'s Slay</h1>\s*</div>', '', html)

# 6. Update GSAP script
# Replace the block of code starting from `// Animate "Let's Slay"` down to `}, "-=0.8");`
# With just the original timeline stuff
gsap_pattern = r'// Animate "Let\'s Slay".*?tl\.to\("\.hero-bg", \{.*?\n      \}, "-=0\.8"\);'

replacement = """tl.to(".hero-bg", {
        scaleY: "100%",
        duration: 3,
        ease: "power2.inOut",
        delay: 0.25,
        onStart: () => {
          animateCounter(document.querySelector(".counter-3"), 2.5);
          animateCounter(document.querySelector(".counter-2"), 3);
          animateCounter(document.querySelector(".counter-1"), 2, 1.5);
        }
      });"""
html = re.sub(gsap_pattern, replacement, html, flags=re.DOTALL)

with open('/Users/apple/Desktop/ome/index.html', 'w') as f:
    f.write(html)
print("Updated index.html")
