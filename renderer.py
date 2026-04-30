import json
import os
from datetime import datetime

def render_brief_html(brief_data):
    brief = brief_data.get("brief", brief_data)
    review = brief_data.get("editorial_review", {})
    
    dir_color = {"up": "#1a5c3a", "down": "#8b1a1a", "neutral": "#6b6355"}
    risk_color = {"HIGH": "#8b1a1a", "MEDIUM": "#8b6914", "LOW": "#1a5c3a"}
    
    market_html = ""
    for d in brief.get("marketData", []):
        color = dir_color.get(d.get("direction", "neutral"), "#6b6355")
        market_html += f"""
        <div style="background:#ede8dc;padding:12px 14px;">
            <div style="font-family:monospace;font-size:9px;letter-spacing:0.12em;text-transform:uppercase;color:#6b6355;margin-bottom:4px;">{d.get('label','')}</div>
            <div style="font-family:monospace;font-size:13px;font-weight:500;color:#0d0d0d;">{d.get('value','')}</div>
            <div style="font-family:monospace;font-size:10px;margin-top:3px;color:{color};">{d.get('change','')}</div>
        </div>"""
    
    sections_html = ""
    for i, s in enumerate(brief.get("sections", [])):
        border = "none" if i == 0 else "1px solid #c8b89a"
        margin = "0 0 8px" if i == 0 else "20px 0 8px"
        padding = "0" if i == 0 else "20px 0 0"
        sections_html += f"""
        <h3 style="font-family:'Playfair Display',Georgia,serif;font-size:16px;font-weight:700;margin:{margin};padding:{padding};border-top:{border};">{s.get('heading','')}</h3>
        <p style="margin:0 0 14px;line-height:1.75;">{s.get('content','')}</p>"""
    
    risks_html = ""
    for r in brief.get("keyRisks", []):
        risks_html += f'<div style="display:flex;gap:8px;padding:5px 0;border-bottom:1px dotted #c8b89a;font-size:13px;line-height:1.5;"><span style="color:#8b1a1a;font-weight:700;flex-shrink:0;">◆</span>{r}</div>'
    
    watchlist_html = ""
    for w in brief.get("watchlist", []):
        watchlist_html += f'<div style="display:flex;gap:8px;padding:5px 0;border-bottom:1px dotted #c8b89a;font-size:13px;line-height:1.5;"><span style="color:#8b1a1a;font-weight:700;flex-shrink:0;">→</span>{w}</div>'
    
    risk_level = brief.get("riskLevel", "MEDIUM")
    risk_col = risk_color.get(risk_level, "#8b6914")
    score = review.get("quality_score", "")
    today = datetime.now().strftime("%A, %B %-d, %Y")
    
    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Senex — {brief.get('headline','Intelligence Brief')}</title>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,400&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;1,8..60,400&display=swap" rel="stylesheet">
<style>
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  body {{ background:#f4f0e8; color:#0d0d0d; font-family:'Source Serif 4',Georgia,serif; font-size:15px; }}
  .print-btn {{ position:fixed; top:20px; right:20px; background:#0d0d0d; color:#f4f0e8; border:none; padding:8px 16px; font-family:monospace; font-size:11px; letter-spacing:0.15em; text-transform:uppercase; cursor:pointer; }}
  @media print {{ .print-btn {{ display:none; }} body {{ background:#fff; }} }}
</style>
</head>
<body>
<button class="print-btn" onclick="window.print()">Print / Save PDF</button>

<div style="max-width:900px;margin:0 auto;padding:3cm 2cm;">

  <!-- MASTHEAD -->
  <div style="border-bottom:3px double #0d0d0d;padding-bottom:16px;margin-bottom:16px;display:flex;justify-content:space-between;align-items:flex-end;">
    <div style="font-family:monospace;font-size:9px;letter-spacing:0.12em;text-transform:uppercase;color:#6b6355;line-height:1.8;">Est. 2025<br/>Intelligence Brief<br/>For Research Use</div>
    <div style="text-align:center;">
      <h1 style="font-family:'Playfair Display',Georgia,serif;font-size:32px;font-weight:900;text-transform:uppercase;letter-spacing:0.05em;">Senex</h1>
      <div style="font-family:monospace;font-size:8px;letter-spacing:0.25em;text-transform:uppercase;color:#6b6355;margin-top:4px;">Geopolitical Market Intelligence</div>
    </div>
    <div style="font-family:monospace;font-size:9px;color:#6b6355;text-align:right;line-height:1.8;">{today}</div>
  </div>

  <!-- REPORT HEADER -->
  <div style="border-bottom:3px double #0d0d0d;padding-bottom:20px;margin-bottom:20px;">
    <div style="font-family:monospace;font-size:9px;letter-spacing:0.3em;text-transform:uppercase;color:#8b1a1a;margin-bottom:8px;">{brief.get('kicker','')}</div>
    <h2 style="font-family:'Playfair Display',Georgia,serif;font-size:28px;font-weight:700;line-height:1.2;margin-bottom:12px;">{brief.get('headline','')}</h2>
    <p style="font-style:italic;color:#6b6355;line-height:1.6;border-left:3px solid #8b1a1a;padding-left:14px;font-size:15px;">{brief.get('deck','')}</p>
    <div style="font-family:monospace;font-size:9px;letter-spacing:0.12em;text-transform:uppercase;color:#6b6355;margin-top:10px;">Senex Intelligence Unit · {today}</div>
  </div>

  <!-- MARKET DATA STRIP -->
  <div style="display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#c8b89a;margin-bottom:24px;">
    {market_html}
  </div>

  <!-- BODY + SIDEBAR -->
  <div style="display:grid;grid-template-columns:2fr 1fr;gap:32px;align-items:start;">
    
    <div style="line-height:1.8;font-size:15px;">
      {sections_html}
    </div>

    <div>
      <div style="background:#ede8dc;border:1px solid #c8b89a;border-top:3px solid #0d0d0d;padding:14px;margin-bottom:14px;">
        <div style="font-family:monospace;font-size:8px;letter-spacing:0.2em;text-transform:uppercase;color:#6b6355;margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid #c8b89a;">Risk Assessment</div>
        <span style="font-family:monospace;font-size:9px;letter-spacing:0.1em;text-transform:uppercase;padding:3px 7px;border:1px solid {risk_col};display:inline-block;margin-bottom:6px;color:{risk_col};">{risk_level} RISK</span>
        <p style="font-size:12px;line-height:1.6;color:#6b6355;">{brief.get('riskRationale','')}</p>
      </div>

      <div style="background:#ede8dc;border:1px solid #c8b89a;border-top:3px solid #0d0d0d;padding:14px;margin-bottom:14px;">
        <div style="font-family:monospace;font-size:8px;letter-spacing:0.2em;text-transform:uppercase;color:#6b6355;margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid #c8b89a;">Key Risks</div>
        {risks_html}
      </div>

      <div style="background:#ede8dc;border:1px solid #c8b89a;border-top:3px solid #0d0d0d;padding:14px;margin-bottom:14px;">
        <div style="font-family:monospace;font-size:8px;letter-spacing:0.2em;text-transform:uppercase;color:#6b6355;margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid #c8b89a;">Watchlist</div>
        {watchlist_html}
      </div>

      {f'''<div style="background:#ede8dc;border:1px solid #c8b89a;border-top:3px solid #0d0d0d;padding:14px;">
        <div style="font-family:monospace;font-size:8px;letter-spacing:0.2em;text-transform:uppercase;color:#6b6355;margin-bottom:8px;padding-bottom:6px;border-bottom:1px solid #c8b89a;">Editorial Score</div>
        <div style="font-family:monospace;font-size:20px;font-weight:500;color:#0d0d0d;">{score}/10</div>
        <p style="font-size:11px;line-height:1.6;color:#6b6355;margin-top:4px;">{review.get("editor_note","")}</p>
      </div>''' if score else ''}
    </div>
  </div>

  <!-- FOOTER -->
  <div style="margin-top:32px;padding-top:12px;border-top:1px solid #c8b89a;font-family:monospace;font-size:9px;color:#6b6355;display:flex;justify-content:space-between;">
    <span>SENEX — For Research Use Only — Analytical/Indicative Data</span>
    <span>{today}</span>
  </div>

</div>
</body>
</html>"""
    
    return html

def render_all_briefs():
    briefs_dir = "briefs"
    output_dir = "briefs/html"
    os.makedirs(output_dir, exist_ok=True)
    
    json_files = [f for f in os.listdir(briefs_dir) if f.endswith(".json")]
    
    if not json_files:
        print("No briefs found in briefs/ folder")
        return
    
    print(f"Rendering {len(json_files)} briefs...\n")
    
    for filename in sorted(json_files):
        filepath = os.path.join(briefs_dir, filename)
        with open(filepath, "r") as f:
            brief_data = json.load(f)
        
        html = render_brief_html(brief_data)
        
        output_filename = filename.replace(".json", ".html")
        output_path = os.path.join(output_dir, output_filename)
        
        with open(output_path, "w") as f:
            f.write(html)
        
        headline = brief_data.get("brief", {}).get("headline", "Unknown")
        print(f"✓ {output_filename}")
        print(f"  {headline[:60]}")
    
    print(f"\nAll briefs rendered to {output_dir}/")
    print("Open any .html file in your browser to view.")

if __name__ == "__main__":
    render_all_briefs()