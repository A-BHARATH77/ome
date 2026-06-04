import re

with open('/Users/apple/Desktop/ome/index.html', 'r') as f:
    html = f.read()

# 1. Find the GSAP scripts block
gsap_pattern = r'(<script src="https://cdn\.jsdelivr\.net/npm/gsap@3\.12\.5/dist/gsap\.min\.js"></script>.*?</script>)'
match = re.search(gsap_pattern, html, flags=re.DOTALL)
if match:
    gsap_block = match.group(1)
    
    # Remove from original location
    html = html.replace(gsap_block, '')
    
    # Change DOMContentLoaded to immediate execution
    gsap_block = gsap_block.replace('document.addEventListener("DOMContentLoaded", () => {', '(() => {')
    gsap_block = gsap_block.replace('});\n\n  </script>', '})();\n  </script>')
    
    # Find insertion point before <script src="head.js"></script>
    insert_idx = html.find('<script src="head.js"></script>')
    if insert_idx != -1:
        html = html[:insert_idx] + gsap_block + "\n    " + html[insert_idx:]
        
    with open('/Users/apple/Desktop/ome/index.html', 'w') as f:
        f.write(html)
    print("Moved GSAP scripts before head.js/body.js and made it run immediately.")
else:
    print("GSAP block not found!")
