import json
with open('grid_work_temp.html', 'r', encoding='utf-8') as f:
    grid_html = f.read()

grid_html_js = json.dumps(grid_html)

injection_script = f"""
                // --- INJECT GRID WORK ---
                const gridHtmlStr = {grid_html_js};
                const framerSections = document.querySelectorAll('section.framer-142v1cj');
                if (framerSections.length > 0) {{
                    const lastSection = framerSections[framerSections.length - 1];
                    const target = lastSection.parentElement.classList.contains('ssr-variant') 
                        ? lastSection.parentElement 
                        : lastSection;
                    
                    const temp = document.createElement('div');
                    temp.innerHTML = gridHtmlStr;
                    target.insertAdjacentElement('afterend', temp.firstElementChild);
                }}
                // ------------------------
"""

with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target_str = "if (main) main.outerHTML = window.pageBodyContent;"
html = html.replace(target_str, target_str + '\n' + injection_script)

dependencies = """
    <!-- Webflow CSS & Styles -->
    <link crossorigin="anonymous" href="https://cdn.prod.website-files.com/699b6466d5f19893993a4bf2/css/monof-template.webflow.shared.ed8969994.css" integrity="sha384-7YlpmUoeN0WqdINU7Tpi28Mn5CX2bsLXtth3eWrSMfs7pFimbnfhPzcEj7Zzk+Dh" rel="stylesheet" type="text/css"/>
    <link href="https://unpkg.com/lenis@1.3.4/dist/lenis.css" rel="stylesheet"/>
    <style>html.w-mod-js:not(.w-mod-ix3) :is(.h2._01, .contact-info.for-button, .bg-change, .menu-wrapper, [data-wf-target*='["699b6466d5f19893993a4bf1","668513fa-96bc-a471-9254-1244961a6485"]'], .preloader, [data-wf-target*='["699b6466d5f19893993a4bf1","ce714b43-ca02-f75e-a30b-e50c0386be7f"]'], .circle-divider, [data-wf-target*='["699b6466d5f19893993a4bf1","11f4fc70-8a2d-088c-43e4-29580902aa2d"]'], [data-wf-target*='["699b6466d5f19893993a4bf1","57b5af3e-8de7-1a3d-0bcc-71e02f1dacc5"]'], .top-text.big, .team-flex, .photo-section, .cta-sm-title._02, .cta-sm-title._03, .cta-sm-title._04, .cta-sm-title._05, .absolute-photo, .video-grid, .cta-sm-title._06, .play-video, .card-stats-side.front, .card-stats-side.back, .pricing-txt._01, .pricing-txt._02, .pricing-txt._03) {visibility: hidden !important;}</style>
    <style>
    .glass::before {
      content: "";
      position: absolute;
      inset: 0;
      border-radius: inherit;
      pointer-events: none;
      background: linear-gradient(
        180deg,
        rgba(255,255,255,0.25) 0%,
        rgba(255,255,255,0.06) 40%,
        transparent 70%
      );
    }
    </style>
"""

webflow_js = """
    <!-- Webflow JS -->
    <script src="https://unpkg.com/lenis@1.3.4/dist/lenis.min.js"></script>
    <script crossorigin="anonymous" integrity="sha256-9/aliU8dGd2tb6OSsuzixeV4y/faTqgFtohetphbbj0=" src="https://d3e54v103j8qbb.cloudfront.net/js/jquery-3.5.1.min.dc5e7f18c8.js?site=699b6466d5f19893993a4bf2" type="text/javascript"></script>
    <script crossorigin="anonymous" integrity="sha384-ar82P9eriV3WGOD8Lkag3kPxxkFE9GSaSPalaC0MRlR/5aACGoFQNfyqt0dNuYvt" src="https://cdn.prod.website-files.com/699b6466d5f19893993a4bf2/js/webflow.schunk.e0c428ff9737f919.js" type="text/javascript"></script>
    <script crossorigin="anonymous" integrity="sha384-yYiFABTm125rQj76PRXHtaj+bUxdrPTq+1UvlD4g3GnxPj1ipgCHX8VPtLdtYUEi" src="https://cdn.prod.website-files.com/699b6466d5f19893993a4bf2/js/webflow.schunk.25099a4fefa544e6.js" type="text/javascript"></script>
    <script crossorigin="anonymous" integrity="sha384-6/R+C9Ue+Qc5OY004ldJc9mD0GFbs04Ut0kV6t86NG4D5+LeFuXnoq8dK1FY2imF" src="https://cdn.prod.website-files.com/699b6466d5f19893993a4bf2/js/webflow.6e875794.53d57b6d7b6754cb.js" type="text/javascript"></script>
"""

html = html.replace('</head>', dependencies + '\n</head>')
html = html.replace('</body>', webflow_js + '\n</body>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print('Done!')
