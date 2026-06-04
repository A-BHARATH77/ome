import re

with open('/Users/apple/Downloads/cg-konpo-lp-reveal/index.html', 'r') as f:
    user_html = f.read()

# Extract <style>
style_match = re.search(r'<style>.*?</style>', user_html, flags=re.DOTALL)
user_styles = style_match.group(0) if style_match else ""

# Extract <section class="hero">...</section>
section_match = re.search(r'<section class="hero">.*?</section>', user_html, flags=re.DOTALL)
user_hero = section_match.group(0) if section_match else ""

# Extract all <script>
script_matches = re.findall(r'<script.*?</script>', user_html, flags=re.DOTALL)
user_scripts = "\n".join(script_matches)

# 2. Modify body.js
with open('/Users/apple/Desktop/ome/body.js', 'r') as f:
    body_js = f.read()

start_str = '<section class="framer-i2anp5" data-framer-name="Hero" id="hero">'
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
        new_body_js = body_js[:start_idx] + user_hero + body_js[end_idx:]
        with open('/Users/apple/Desktop/ome/body.js', 'w') as f:
            f.write(new_body_js)
        print("Replaced Hero in body.js")
    else:
        print("Could not find end of Hero section in body.js")
else:
    print("Hero section not found in body.js")

# 3. Modify index.html to add styles and scripts
with open('/Users/apple/Desktop/ome/index.html', 'r') as f:
    index_html = f.read()

if 'PP Neue Montreal' not in index_html:
    # Add styles to head
    head_end = index_html.find('</head>')
    if head_end != -1:
        index_html = index_html[:head_end] + user_styles + "\n" + index_html[head_end:]

    # Add scripts to body end
    body_end = index_html.find('</body>')
    if body_end != -1:
        index_html = index_html[:body_end] + user_scripts + "\n" + index_html[body_end:]

    with open('/Users/apple/Desktop/ome/index.html', 'w') as f:
        f.write(index_html)
    print("Added styles and scripts to index.html")
else:
    print("index.html already modified")
