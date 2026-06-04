import re

with open('/Users/apple/Desktop/ome/index.html', 'r') as f:
    html = f.read()

# Locate the remaining GSAP parts (SplitText and the inline script)
# They start around line 915.
# Let's find `<script src="https://cdn.jsdelivr.net/npm/gsap-trial@3.12.5/dist/SplitText.min.js"></script>`
start_str = '<script src="https://cdn.jsdelivr.net/npm/gsap-trial@3.12.5/dist/SplitText.min.js"></script>'
start_idx = html.find(start_str)

if start_idx != -1:
    # Find the end of the inline script
    end_str = '})();\n  </script>'
    end_idx = html.find(end_str, start_idx)
    if end_idx == -1:
        # maybe it is still DOMContentLoaded?
        end_str_old = '});\n\n  </script>'
        end_idx = html.find(end_str_old, start_idx)
        if end_idx != -1:
            end_idx += len(end_str_old)
        else:
            print("End of GSAP script not found!")
    else:
        end_idx += len(end_str)
        
    if end_idx != -1:
        gsap_script = html[start_idx:end_idx]
        
        # Remove it from the original location
        html = html[:start_idx] + html[end_idx:]
        
        # Fix the DOMContentLoaded to immediate IIFE if not already done
        gsap_script = gsap_script.replace('document.addEventListener("DOMContentLoaded", () => {', '(() => {')
        gsap_script = gsap_script.replace('});\n\n  </script>', '})();\n  </script>')
        
        # Now find where to insert it. We want it right before `<script src="head.js"></script>`
        insert_idx = html.find('<script src="head.js"></script>')
        if insert_idx != -1:
            html = html[:insert_idx] + gsap_script + "\n    " + html[insert_idx:]
            
            with open('/Users/apple/Desktop/ome/index.html', 'w') as f:
                f.write(html)
            print("Successfully moved SplitText and inline GSAP script.")
else:
    print("SplitText script not found.")
