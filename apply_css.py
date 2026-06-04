with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

custom_css = """
    <!-- Custom Layout Overrides -->
    <style>
      /* Main layout: side by side */
      .grid-work {
          display: flex !important;
          flex-direction: row !important;
          justify-content: space-between !important;
          align-items: flex-start !important;
          gap: 5% !important;
          padding: 4rem 5% !important;
          max-width: 1400px;
          margin: 0 auto;
      }

      /* Left side: Sticky at center */
      .grid-work .sticky-lft {
          width: 35% !important;
          position: sticky !important;
          top: 50% !important;
          transform: translateY(-50%) !important;
          display: flex !important;
          flex-direction: column !important;
          align-items: flex-start !important;
          height: auto !important; 
      }

      /* Right side: Scrolling images */
      .grid-work .work-main {
          width: 60% !important;
          display: flex !important;
          flex-direction: column !important;
      }

      /* Override internal grid so images stack cleanly */
      .work-main .wrok-wrapper {
          display: flex !important;
          flex-direction: column !important;
          gap: 4rem !important;
      }
      
      .work-card {
         width: 100% !important;
         margin: 0 !important;
      }
      
      /* Mobile responsiveness */
      @media (max-width: 991px) {
          .grid-work {
              flex-direction: column !important;
              padding: 2rem 5% !important;
          }
          .grid-work .sticky-lft {
              width: 100% !important;
              position: relative !important;
              top: 0 !important;
              transform: none !important;
              margin-bottom: 2rem !important;
          }
          .grid-work .work-main {
              width: 100% !important;
          }
      }
    </style>
"""

html = html.replace('</head>', custom_css + '\n</head>')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("CSS overrides applied.")
