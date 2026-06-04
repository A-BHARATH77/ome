import re

with open('index.html', 'r') as f:
    html = f.read()

# Remove duplicate <style>... \n </head> \n <body> \n <section class="hero"> that might have been accidentally inserted
# Wait, let's just find the first <style> and everything before it, up to </head>

# It's safer to reconstruct.
# 1. Get the original stuff before line 458 (which was the end of the original <style>)
# We know the original style ends with:
#           .grid-work .work-main {
#               width: 100% !important;
#               flex: unset !important;
#               padding-left: 0 !important;
#           }
#       }
#     </style>
# 
# Let's find this.
marker_1 = "padding-left: 0 !important;\n          }\n      }\n    </style>"
idx_1 = html.find(marker_1)
if idx_1 != -1:
    idx_1 += len(marker_1)
    
part_1 = html[:idx_1]

# Now we need the user styles
with open('user_hero.html', 'r') as f:
    user_html = f.read()

style_match = re.search(r'<style>.*?</style>', user_html, flags=re.DOTALL)
user_style = style_match.group(0) if style_match else ""

# Hide framer hero
hide_hero_css = "<style>.framer-i2anp5 { display: none !important; }</style>"

# Now find the <div id="main"> 
idx_main = html.find('<div id="main">')

part_2 = "\n</head>\n<body>\n"

# Get new hero section
hero_match = re.search(r'<section class="hero">.*?</section>', user_html, flags=re.DOTALL)
new_hero = hero_match.group(0) if hero_match else ""

# Get the rest of the original body starting from <div id="main"> to the end, BUT remove duplicate scripts
part_3 = html[idx_main:]

# Remove any extra </body> or scripts we injected earlier, we will just inject them freshly at the very end
# Let's find the FIRST window.dispatchEvent(new Event('load'));
idx_load = part_3.find("window.dispatchEvent(new Event('load'));")
if idx_load != -1:
    idx_end_script = part_3.find("})();\n    </script>", idx_load)
    if idx_end_script != -1:
        idx_end_script += len("})();\n    </script>")
        # Also include the Webflow JS
        idx_webflow = part_3.find('src="https://cdn.prod.website-files.com', idx_end_script)
        if idx_webflow != -1:
            idx_after_webflow = part_3.find('</script>', part_3.find('</script>', part_3.find('</script>', idx_webflow)+1)+1)
            if idx_after_webflow != -1:
                idx_after_webflow += len("</script>")
                part_3_clean = part_3[:idx_after_webflow]
            else:
                part_3_clean = part_3
        else:
            part_3_clean = part_3
else:
    part_3_clean = part_3

# Extract user scripts
scripts = re.findall(r'<script.*?</script>', user_html, flags=re.DOTALL)
user_scripts = "\n".join(scripts)

final_html = part_1 + "\n" + user_style + "\n" + hide_hero_css + part_2 + new_hero + "\n" + part_3_clean + "\n" + user_scripts + "\n</body>\n</html>"

with open('index_fixed.html', 'w') as f:
    f.write(final_html)
print("Created index_fixed.html")

