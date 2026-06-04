import re

# Read the new hero section from user_hero.html
with open('/Users/apple/Desktop/ome/user_hero.html', 'r') as f:
    user_html = f.read()

section_match = re.search(r'<section class="hero">.*?</section>', user_html, flags=re.DOTALL)
new_hero = section_match.group(0) if section_match else ""

# Modify body.js
with open('/Users/apple/Desktop/ome/body.js', 'r') as f:
    body_js = f.read()

# Because we already injected <section class="hero"> previously, we can find it
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
        new_body_js = body_js[:start_idx] + new_hero + body_js[end_idx:]
        with open('/Users/apple/Desktop/ome/body.js', 'w') as f:
            f.write(new_body_js)
        print("Replaced Hero in body.js with the new one")
    else:
        print("Could not find end of Hero section in body.js")
else:
    print("Hero section not found in body.js")
