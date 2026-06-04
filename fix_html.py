with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = '<html lang="en" data-redirect-timezone="1" dir="ltr">'
replacement = '<html lang="en" data-redirect-timezone="1" dir="ltr" data-wf-domain="monof-template.webflow.io" data-wf-page="699b6466d5f19893993a4bf1" data-wf-site="699b6466d5f19893993a4bf2">'

html = html.replace(target, replacement)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Updated HTML tag attributes.")
