import json
import re

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Read the grid work HTML
with open('grid_work_temp.html', 'r', encoding='utf-8') as f:
    grid_html = f.read()

grid_html_js = json.dumps(grid_html)

new_injection_script = f"""
                // --- INJECT GRID WORK ---
                const gridHtmlStr = {grid_html_js};
                
                // We use a MutationObserver to wait for Framer's hydration to finish,
                // or fallback to a timeout.
                setTimeout(() => {{
                    const framerSections = document.querySelectorAll('section.framer-142v1cj');
                    if (framerSections.length > 0) {{
                        const lastSection = framerSections[framerSections.length - 1];
                        const target = lastSection.parentElement.classList.contains('ssr-variant') 
                            ? lastSection.parentElement 
                            : lastSection;
                        
                        // Check if already injected
                        if (!document.querySelector('.grid-work')) {{
                            const temp = document.createElement('div');
                            temp.innerHTML = gridHtmlStr;
                            target.insertAdjacentElement('afterend', temp.firstElementChild);
                            
                            // Restart Webflow so animations work on the new element
                            if (window.Webflow) {{
                                window.Webflow.destroy();
                                window.Webflow.ready();
                                if (window.Webflow.require('ix2')) {{
                                    window.Webflow.require('ix2').init();
                                }}
                            }}
                        }}
                    }}
                }}, 1500);
                // ------------------------
"""

# Use regex to find the old injection block, then replace with string replace
old_pattern = re.compile(r'// --- INJECT GRID WORK ---.*?// ------------------------', re.DOTALL)
match = old_pattern.search(html)
if match:
    old_text = match.group(0)
    html = html.replace(old_text, new_injection_script.strip())

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Successfully updated index.html to inject after hydration.')
