import re
import json

with open('Mono.html', 'r', encoding='utf-8') as f:
    mono_content = f.read()

# Extract Section 3 (Services)
# Match specifically the section that contains "(Services)"
section_match = re.search(r'(?s)<section[^>]*class="section"[^>]*>.*?\(Services\).*?</section>', mono_content)

if not section_match:
    # Fallback to the known index if content match is tricky
    # Match based on the exact class "section" (no other classes)
    sections = re.findall(r'(?s)<section[^>]*class="section"[^>]*>.*?</section>', mono_content)
    # Based on previous find_sections.py, it was the first one with EXACTLY class="section"
    for s in sections:
        if '(Services)' in s:
            section_html = s
            break
else:
    section_html = section_match.group(0)

# Check for the transition immediately following the Services section
# Usually a rounder-wrapper
end_pos = mono_content.find(section_html) + len(section_html)
transition_match = re.search(r'(?s)^\s*(<div data-w-id="[^"]*" class="rounder-wrapper">.*?</div></div>)', mono_content[end_pos:end_pos+1000])
if transition_match:
    section_html += transition_match.group(1)

section_json = json.dumps(section_html)

with open('index.html', 'r', encoding='utf-8') as f:
    index_html = f.read()

# Injection script part
# We look for framer-12jl4kx
injection_code = f"""
                // --- INJECT SERVICES SECTION BELOW framer-12jl4kx ---
                const servicesSectionHtml = {section_json};
                
                setTimeout(() => {{
                    const targetSection = document.querySelector('.framer-12jl4kx');
                    // Check if target exists and if we haven't already injected this specific content
                    if (targetSection && !document.querySelector('.service-grid')) {{
                        const temp = document.createElement('div');
                        temp.innerHTML = servicesSectionHtml;
                        
                        // Insert all children of temp after targetSection
                        let lastInserted = targetSection;
                        while (temp.firstChild) {{
                            const node = temp.firstChild;
                            lastInserted.insertAdjacentElement('afterend', node);
                            lastInserted = node;
                        }}

                        // Restart Webflow IX2 for animations
                        if (window.Webflow) {{
                            window.Webflow.destroy();
                            window.Webflow.ready();
                            if (window.Webflow.require('ix2')) {{
                                window.Webflow.require('ix2').init();
                            }}
                        }}
                    }}
                }}, 2000);
                // -----------------------------------------------------
"""

# We'll insert it near the other injection blocks
marker = "// --- INJECT GRID WORK ---"
if marker not in index_html:
    marker = "// Re-execute scripts"

index_marker = index_html.find(marker)

if index_marker != -1:
    new_html = index_html[:index_marker] + injection_code + index_html[index_marker:]
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)
    print("Successfully updated index.html with Services section")
else:
    print("Marker not found in index.html")
