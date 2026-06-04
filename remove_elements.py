import re

with open('/Users/apple/Desktop/ome/index.html', 'r') as f:
    html = f.read()

# Remove sidebar HTML
sidebar_pattern = r'<div class="sidebar">.*?</div>\s*</div>'
html = re.sub(sidebar_pattern, '', html, flags=re.DOTALL)

# Also there's a standalone <div class="sidebar">...</div> possibly.
# Let's be more precise.
sidebar_pattern2 = r'\s*<div class="sidebar">\s*<div class="logo">.*?<div class="divider"></div>\s*</div>'
html = re.sub(sidebar_pattern2, '', html, flags=re.DOTALL)

# Remove hero-footer HTML
footer_pattern = r'\s*<div class="hero-footer">\s*<h2>Watch showreel</h2>\s*</div>'
html = re.sub(footer_pattern, '', html, flags=re.DOTALL)

# Make images bigger in CSS
html = html.replace('width: 20%;', 'width: 28%;')
# The user wants "all uniform size". They are uniform already due to aspect-ratio 5/3, but 4/3 might look bigger.
html = html.replace('aspect-ratio: 5/3;', 'aspect-ratio: 4/3;')

# Remove GSAP logo animation just in case it errors, although GSAP usually just warns.
# We'll leave GSAP alone to be safe unless it causes issues. Actually, GSAP handles missing elements gracefully.

with open('/Users/apple/Desktop/ome/index.html', 'w') as f:
    f.write(html)
print("Removed sidebar, hero-footer, and made images bigger.")
