import re

# 1. Hide the old hero in index.html and inject new hero before #main
with open('/Users/apple/Desktop/ome/index.html', 'r') as f:
    index_html = f.read()

# Add CSS to hide framer hero
if '.framer-i2anp5 { display: none !important; }' not in index_html:
    style_end = index_html.find('</style>')
    if style_end != -1:
        css_addition = "\n        .framer-i2anp5 { display: none !important; }\n"
        index_html = index_html[:style_end] + css_addition + index_html[style_end:]

# Get the new hero from user_hero.html
with open('/Users/apple/Desktop/ome/user_hero.html', 'r') as f:
    user_html = f.read()
section_match = re.search(r'<section class="hero">.*?</section>', user_html, flags=re.DOTALL)
new_hero = section_match.group(0) if section_match else ""

# Inject new hero into index.html before <div id="main">
if new_hero and '<section class="hero">' not in index_html:
    main_idx = index_html.find('<div id="main">')
    if main_idx != -1:
        index_html = index_html[:main_idx] + new_hero + "\n" + index_html[main_idx:]

with open('/Users/apple/Desktop/ome/index.html', 'w') as f:
    f.write(index_html)
print("Updated index.html to include the new hero and hide the old one.")

# 2. Remove the new hero from body.js to avoid duplication/flashes
with open('/Users/apple/Desktop/ome/body.js', 'r') as f:
    body_js = f.read()

start_str = '<section class="hero">'
start_idx = body_js.find(start_str)

if start_idx != -1:
    depth = 0
    i = start_idx
    end_idx = -1
    while i < len(body_js):
        if body_js.startswith('<section', i):
            depth += 1
        elif body_js.startswith('</section>', i):
            depth -= 1
            if depth == 0:
                end_idx = i + len('</section>')
                break
        i += 1

    if end_idx != -1:
        # Just remove it completely
        new_body_js = body_js[:start_idx] + body_js[end_idx:]
        with open('/Users/apple/Desktop/ome/body.js', 'w') as f:
            f.write(new_body_js)
        print("Removed duplicated new hero from body.js")
    else:
        print("Could not find end of Hero section in body.js")
else:
    print("New Hero section not found in body.js")

