import re

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Locate the servicesSectionHtml string
# It's a long string containing <section class="section">...
match = re.search(r'(?s)const servicesSectionHtml = "(.*?)";', content)

if match:
    original_html = match.group(1)
    
    # Remove the rounder-wrapper part
    # Pattern: <div data-w-id="..." class="rounder-wrapper">...</div></div>
    # Note: The string in JS has escaped quotes \"
    clean_html = re.sub(r'(?s)<div data-w-id=\\"[^\\"]*\\" class=\\"rounder-wrapper\\">.*?</div></div>', '', original_html)
    
    # Also remove any trailing <div class=\"spacer-xxl\"></div> if it exists at the end of the section
    clean_html = re.sub(r'<div class=\\"spacer-xxl\\"></div></section>', '</section>', clean_html)

    new_line = f'const servicesSectionHtml = "{clean_html}";'
    new_content = content.replace(match.group(0), new_line)
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Successfully cleaned servicesSectionHtml")
else:
    print("servicesSectionHtml not found")
