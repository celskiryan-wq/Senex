import { useState } from "react";

function openInTab(brief, today) {
  const riskClass = brief.riskLevel==="HIGH"?"risk-high":brief.riskLevel==="LOW"?"risk-low":"risk-med";
  const html = `<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Senex — ${(brief.headline||"Intelligence Brief").replace(/"/g,"&quot;")}</title>
<style>
  @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=Source+Serif+4:ital,opsz,wght@0,8..60,400;1,8..60,400&display=swap');
  *{margin:0;padding:0;box-sizing:border-box}
  body{background:#f4f0e8;color:#0d0d0d;font-family:'Source Serif 4',Georgia,serif;padding:3cm;font-size:10.5pt;max-width:800px;margin:0 auto}
  .masthead{border-bottom:3px double #0d0d0d;padding-bottom:14px;margin-bottom:14px;display:flex;justify-content:space-between;align-items:flex-end}
  h1{font-family:'Playfair Display',serif;font-size:24pt;font-weight:900;text-transform:uppercase;letter-spacing:0.05em}
  .masthead-sub{font-family:monospace;font-size:6pt;letter-spacing:0.2em;text-transform:uppercase;color:#6b6355;margin-top:3px}
  .meta{font-family:monospace;font-size:6.5pt;color:#6b6355;line-height:1.8}
  .kicker{font-family:monospace;font-size:6.5pt;letter-spacing:0.25em;text-transform:uppercase;color:#8b1a1a;margin-bottom:8px}
  h2{font-family:'Playfair Display',serif;font-size:20pt;font-weight:700;line-height:1.2;margin-bottom:10px}
  .deck{font-style:italic;color:#6b6355;line-height:1.6;border-left:3px solid #8b1a1a;padding-left:12px;margin-bottom:10px}
  .byline{font-family:monospace;font-size:6pt;letter-spacing:0.12em;text-transform:uppercase;color:#6b6355;margin-bottom:16px}
  .report-header{border-bottom:3px double #0d0d0d;padding-bottom:16px;margin-bottom:16px}
  .data-strip{display:grid;grid-template-columns:repeat(4,1fr);gap:1px;background:#c8b89a;border:1px solid #c8b89a;margin-bottom:20px}
  .data-cell{background:#ede8dc;padding:8px 10px}
  .data-label{font-family:monospace;font-size:5.5pt;letter-spacing:0.12em;text-transform:uppercase;color:#6b6355;margin-bottom:3px}
  .data-value{font-family:monospace;font-size:9pt;font-weight:500}
  .data-change{font-family:monospace;font-size:6.5pt;margin-top:2px}
  .up{color:#1a5c3a}.down{color:#8b1a1a}.neutral{color:#6b6355}
  .body-grid{display:grid;grid-template-columns:2fr 1fr;gap:24px}
  h3{font-family:'Playfair Display',serif;font-size:11pt;font-weight:700;margin:14px 0 5px;padding-top:14px;border-top:1px solid #c8b89a}
  h3.first{margin-top:0;padding-top:0;border-top:none}
  p{margin-bottom:10px;line-height:1.75}
  .sidebar-box{background:#ede8dc;border:1px solid #c8b89a;border-top:3px solid #0d0d0d;padding:10px;margin-bottom:12px}
  .sidebar-title{font-family:monospace;font-size:5.5pt;letter-spacing:0.2em;text-transform:uppercase;color:#6b6355;margin-bottom:7px;padding-bottom:5px;border-bottom:1px solid #c8b89a}
  .risk-badge{font-family:monospace;font-size:6pt;letter-spacing:0.1em;text-transform:uppercase;padding:2px 6px;border:1px solid currentColor;display:inline-block;margin-bottom:5px}
  .risk-high{color:#8b1a1a}.risk-med{color:#8b6914}.risk-low{color:#1a5c3a}
  .sidebar-item{display:flex;gap:6px;padding:4px 0;border-bottom:1px dotted #c8b89a;font-size:8.5pt;line-height:1.5}
  .sidebar-item:last-child{border-bottom:none}
  .bullet{color:#8b1a1a;font-weight:700;flex-shrink:0}
  .footer{margin-top:24px;padding-top:10px;border-top:1px solid #c8b89a;font-family:monospace;font-size:6pt;color:#6b6355;display:flex;justify-content:space-between}
  .print-btn{position:fixed;top:20px;right:20px;background:#0d0d0d;color:#f4f0e8;border:none;padding:8px 16px;font-family:monospace;font-size:0.6rem;letter-spacing:0.15em;text-transform:uppercase;cursor:pointer}
  @media print{.print-btn{display:none}body{background:#fff;padding:1.5cm}}
</style>
</head>
<body>
<button class="print-btn" onclick="window.print()">Print / Save PDF</button>

<div class="masthead">
  <div class="meta">Est. 2025<br/>Intelligence Brief<br/>For Research Use</div>
  <div style="text-align:center">
    <h1>Senex</h1>
    <div class="masthead-sub">Geopolitical Market Intelligence</div>
  </div>
  <div class="meta" style="text-align:right">${today}</div>
</div>

<div class="report-header">
  <div class="kicker">${brief.kicker||""}</div>
  <h2>${brief.headline||""}</h2>
  <div class="deck">${brief.deck||""}</div>
  <div class="byline">Senex Intelligence Unit · ${today}</div>
</div>

<div class="data-strip">
  ${(brief.marketData||[]).map(d=>`
  <div class="data-cell">
    <div class="data-label">${d.label}</div>
    <div class="data-value">${d.value}</div>
    <div class="data-change ${d.direction||"neutral"}">${d.change}</div>
  </div>`).join("")}
</div>

<div class="body-grid">
  <div>
    ${(brief.sections||[]).map((s,i)=>`
    <h3 class="${i===0?"first":""}">${s.heading}</h3>
    <p>${s.content}</p>`).join("")}
  </div>
  <div>
    <div class="sidebar-box">
      <div class="sidebar-title">Risk Assessment</div>
      <span class="risk-badge ${riskClass}">${brief.riskLevel||"MEDIUM"} RISK</span>
      <p style="font-size:8pt;color:#6b6355;line-height:1.6;margin-top:5px">${brief.riskRationale||""}</p>
    </div>
    <div class="sidebar-box">
      <div class="sidebar-title">Key Risks</div>
      ${(brief.keyRisks||[]).map(r=>`<div class="sidebar-item"><span class="bullet">◆</span>${r}</div>`).join("")}
    </div>
    <div class="sidebar-box">
      <div class="sidebar-title">Watchlist</div>
      ${(brief.watchlist||[]).map(w=>`<div class="sidebar-item"><span class="bullet">→</span>${w}</div>`).join("")}
    </div>
  </div>
</div>

<div class="footer">
  <span>SENEX — For Research Use Only — Analytical/Indicative Data</span>
  <span>${today}</span>
</div>
</body>
</html>`;
  const blob = new Blob([html], {type:"text/html"});
  const url = URL.createObjectURL(blob);
  window.open(url, "_blank");
}

const REGIONS = ["East Asia / Pacific","Middle East / North Africa","Europe / Russia","Sub-Saharan Africa","South Asia","Latin America","North America","Global / Multi-regional"];
const DEPTHS = [{v:"brief",l:"Brief (1–2 min read)"},{v:"standard",l:"Standard (3–5 min read)"},{v:"deep",l:"Deep Dive (8–12 min read)"}];
const AUDIENCES = [{v:"think-tank",l:"Think Tank / Policy"},{v:"academic",l:"Academic"},{v:"investor",l:"Institutional Investor"},{v:"journalist",l:"Analyst / Journalist"}];

const inputStyle = {background:"#ede8dc",border:"1px solid #c8b89a",borderBottom:"2px solid #0d0d0d",padding:"0.6rem 0.8rem",fontFamily:"'Source Serif 4',Georgia,serif",fontSize:"0.9rem",color:"#0d0d0d",outline:"none",width:"100%",boxSizing:"border-box"};
const selStyle = {...inputStyle};

export default function Senex() {
  const [event, setEvent] = useState("");
  const [region, setRegion] = useState("");
  const [sectors, setSectors] = useState("");
  const [depth, setDepth] = useState("standard");
  const [audience, setAudience] = useState("think-tank");
  const [loading, setLoading] = useState(false);
  const [brief, setBrief] = useState(null);
  const [error, setError] = useState("");

  const today = new Date().toLocaleDateString("en-US",{weekday:"long",month:"long",day:"numeric",year:"numeric"});

  const depthInstructions = {
    brief: "Write concisely. 2–3 paragraphs total. Focus on immediate market impact.",
    standard: "Write a thorough analysis with 4–5 paragraphs covering context, market implications, and outlook.",
    deep: "Write an academically rigorous analysis with historical context, theoretical frameworks, multi-scenario outlook, and policy implications. 6–8 paragraphs."
  };

  const audienceInstructions = {
    "think-tank": "The audience is policy researchers. Use precise geopolitical terminology, reference international frameworks or precedents, and connect to policy implications.",
    academic: "The audience is academic researchers. Adopt a scholarly register, reference theoretical frameworks, and suggest research questions.",
    investor: "The audience is institutional investors. Focus on actionable market intelligence, risk-adjusted positioning, and sector-specific exposure.",
    journalist: "The audience is financial journalists. Balance accessibility with depth, include concrete data points and clear causal narratives."
  };

  async function generate() {
    if (!event.trim()) { setError("Please describe a geopolitical event."); return; }
    setError(""); setLoading(true); setBrief(null);

    const prompt = `You are a senior geopolitical market analyst. Analyze the following event and produce a structured intelligence brief.

EVENT: ${event}
REGION: ${region || "Not specified"}
FOCUS SECTORS: ${sectors || "All relevant sectors"}
DEPTH: ${depthInstructions[depth]}
AUDIENCE: ${audienceInstructions[audience]}

Respond ONLY with valid JSON. No markdown, no backticks, no preamble. Use this exact structure:
{
  "kicker": "Brief category label e.g. ENERGY MARKETS — EAST ASIA",
  "headline": "Sharp editorial headline max 12 words",
  "deck": "One-sentence analytical summary capturing the key tension 25-35 words",
  "marketData": [
    {"label": "Asset name", "value": "Indicative level", "change": "Directional impact", "direction": "up|down|neutral"},
    {"label": "Asset name", "value": "Indicative level", "change": "Directional impact", "direction": "up|down|neutral"},
    {"label": "Asset name", "value": "Indicative level", "change": "Directional impact", "direction": "up|down|neutral"},
    {"label": "Asset name", "value": "Indicative level", "change": "Directional impact", "direction": "up|down|neutral"}
  ],
  "sections": [
    {"heading": "Section heading", "content": "Full paragraph..."},
    {"heading": "Section heading", "content": "Full paragraph..."},
    {"heading": "Section heading", "content": "Full paragraph..."}
  ],
  "keyRisks": ["Risk 1", "Risk 2", "Risk 3"],
  "watchlist": ["Asset or indicator 1", "Asset or indicator 2", "Asset or indicator 3"],
  "riskLevel": "HIGH",
  "riskRationale": "One sentence explaining the risk rating"
}`;

    try {
      const res = await fetch("https://api.anthropic.com/v1/messages", {
        method: "POST",
        headers: {
          "content-type": "application/json",
          "anthropic-version": "2023-06-01",
          "anthropic-dangerous-direct-browser-access": "true",
          "x-api-key": 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,
        },
        body: JSON.stringify({
          model: "claude-sonnet-4-20250514",
          max_tokens: 4000,
          messages: [{ role: "user", content: prompt }]
        })
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data?.error?.message || "API error " + res.status);

      const raw = data.content.map(b => b.type === "text" ? b.text : "").join("");
      const match = raw.match(/\{[\s\S]*\}/);
      if (!match) throw new Error("No JSON in response");
      setBrief(JSON.parse(match[0]));
    } catch(e) {
      setError("Error: " + e.message);
    } finally {
      setLoading(false);
    }
  }

  const dirColor = d => d === "up" ? "#1a5c3a" : d === "down" ? "#8b1a1a" : "#6b6355";

  return (
    <div style={{background:"#f4f0e8",minHeight:"100vh",fontFamily:"Georgia,serif",color:"#0d0d0d"}}>

      {/* MASTHEAD */}
      <header style={{borderBottom:"3px double #0d0d0d",padding:"1.5rem 2rem 1rem",display:"flex",justifyContent:"space-between",alignItems:"flex-end"}}>
        <div style={{fontFamily:"monospace",fontSize:"0.6rem",letterSpacing:"0.1em",textTransform:"uppercase",color:"#6b6355",lineHeight:1.8}}>
          Est. 2025<br/>Intelligence Brief
        </div>
        <div style={{textAlign:"center"}}>
          <h1 style={{fontFamily:"Georgia,serif",fontSize:"2rem",fontWeight:900,textTransform:"uppercase",letterSpacing:"0.05em",margin:0}}>Senex</h1>
          <div style={{fontFamily:"monospace",fontSize:"0.55rem",letterSpacing:"0.25em",textTransform:"uppercase",color:"#6b6355",marginTop:"0.3rem"}}>Geopolitical Market Intelligence</div>
        </div>
        <div style={{fontFamily:"monospace",fontSize:"0.6rem",color:"#6b6355",lineHeight:1.8,textAlign:"right"}}>
          {new Date().toLocaleDateString("en-US",{month:"long",day:"numeric",year:"numeric"})}
        </div>
      </header>

      <div style={{maxWidth:860,margin:"0 auto",padding:"0 1.5rem 4rem"}}>

        {/* INPUT FORM */}
        {!brief && (
          <div style={{padding:"2rem 0"}}>
            <div style={{fontFamily:"monospace",fontSize:"0.58rem",letterSpacing:"0.25em",textTransform:"uppercase",color:"#6b6355",marginBottom:"1rem"}}>▸ Generate Intelligence Brief</div>

            <div style={{marginBottom:"1rem"}}>
              <div style={{fontFamily:"monospace",fontSize:"0.58rem",letterSpacing:"0.12em",textTransform:"uppercase",color:"#6b6355",marginBottom:"0.4rem"}}>Geopolitical Event</div>
              <textarea
                value={event}
                onChange={e => setEvent(e.target.value)}
                placeholder="e.g. China imposes new export controls on rare earth minerals amid escalating US trade tensions..."
                style={{...inputStyle,resize:"vertical",minHeight:90,lineHeight:1.6}}
              />
            </div>

            <div style={{display:"grid",gridTemplateColumns:"1fr 1fr",gap:"1rem",marginBottom:"1.2rem"}}>
              <div>
                <div style={{fontFamily:"monospace",fontSize:"0.58rem",letterSpacing:"0.12em",textTransform:"uppercase",color:"#6b6355",marginBottom:"0.4rem"}}>Region</div>
                <select value={region} onChange={e=>setRegion(e.target.value)} style={selStyle}>
                  <option value="">Select region...</option>
                  {REGIONS.map(r=><option key={r}>{r}</option>)}
                </select>
              </div>
              <div>
                <div style={{fontFamily:"monospace",fontSize:"0.58rem",letterSpacing:"0.12em",textTransform:"uppercase",color:"#6b6355",marginBottom:"0.4rem"}}>Focus Sectors (optional)</div>
                <input value={sectors} onChange={e=>setSectors(e.target.value)} placeholder="e.g. Energy, Defense, Semiconductors" style={inputStyle}/>
              </div>
              <div>
                <div style={{fontFamily:"monospace",fontSize:"0.58rem",letterSpacing:"0.12em",textTransform:"uppercase",color:"#6b6355",marginBottom:"0.4rem"}}>Analysis Depth</div>
                <select value={depth} onChange={e=>setDepth(e.target.value)} style={selStyle}>
                  {DEPTHS.map(d=><option key={d.v} value={d.v}>{d.l}</option>)}
                </select>
              </div>
              <div>
                <div style={{fontFamily:"monospace",fontSize:"0.58rem",letterSpacing:"0.12em",textTransform:"uppercase",color:"#6b6355",marginBottom:"0.4rem"}}>Audience</div>
                <select value={audience} onChange={e=>setAudience(e.target.value)} style={selStyle}>
                  {AUDIENCES.map(a=><option key={a.v} value={a.v}>{a.l}</option>)}
                </select>
              </div>
            </div>

            <button
              onClick={generate}
              disabled={loading}
              style={{background:loading?"#6b6355":"#0d0d0d",color:"#f4f0e8",border:"none",padding:"0.8rem 2rem",fontFamily:"monospace",fontSize:"0.65rem",letterSpacing:"0.2em",textTransform:"uppercase",cursor:loading?"not-allowed":"pointer"}}
            >
              {loading ? "Analyzing..." : "Generate Brief"}
            </button>

            {error && (
              <div style={{marginTop:"1rem",background:"#fff0f0",border:"1px solid #8b1a1a",borderLeft:"4px solid #8b1a1a",padding:"0.8rem 1rem",fontSize:"0.85rem",color:"#8b1a1a"}}>
                {error}
              </div>
            )}
          </div>
        )}

        {/* OUTPUT */}
        {brief && (
          <div style={{paddingTop:"2rem"}}>

            {/* Header */}
            <div style={{borderBottom:"3px double #0d0d0d",paddingBottom:"1.5rem",marginBottom:"1.5rem"}}>
              <div style={{fontFamily:"monospace",fontSize:"0.55rem",letterSpacing:"0.3em",textTransform:"uppercase",color:"#8b1a1a",marginBottom:"0.5rem"}}>{brief.kicker}</div>
              <h2 style={{fontFamily:"Georgia,serif",fontSize:"1.8rem",fontWeight:700,lineHeight:1.2,marginBottom:"0.8rem"}}>{brief.headline}</h2>
              <p style={{fontSize:"1rem",fontStyle:"italic",color:"#6b6355",lineHeight:1.6,borderLeft:"3px solid #8b1a1a",paddingLeft:"1rem",margin:0}}>{brief.deck}</p>
              <div style={{fontFamily:"monospace",fontSize:"0.55rem",letterSpacing:"0.12em",textTransform:"uppercase",color:"#6b6355",marginTop:"0.8rem"}}>Senex Intelligence Unit · {today}</div>
            </div>

            {/* Market data */}
            <div style={{display:"grid",gridTemplateColumns:"repeat(4,1fr)",gap:1,background:"#c8b89a",border:"1px solid #c8b89a",marginBottom:"2rem"}}>
              {(brief.marketData||[]).map((d,i)=>(
                <div key={i} style={{background:"#ede8dc",padding:"0.8rem 1rem"}}>
                  <div style={{fontFamily:"monospace",fontSize:"0.5rem",letterSpacing:"0.12em",textTransform:"uppercase",color:"#6b6355",marginBottom:"0.25rem"}}>{d.label}</div>
                  <div style={{fontFamily:"monospace",fontSize:"0.85rem",fontWeight:500}}>{d.value}</div>
                  <div style={{fontFamily:"monospace",fontSize:"0.65rem",marginTop:"0.2rem",color:dirColor(d.direction)}}>{d.change}</div>
                </div>
              ))}
            </div>

            {/* Body + sidebar */}
            <div style={{display:"grid",gridTemplateColumns:"2fr 1fr",gap:"2rem",alignItems:"start"}}>
              <div style={{lineHeight:1.8,fontSize:"0.95rem"}}>
                {(brief.sections||[]).map((s,i)=>(
                  <div key={i}>
                    <h3 style={{fontFamily:"Georgia,serif",fontSize:"1.05rem",fontWeight:700,margin:i===0?"0 0 0.5rem":"1.5rem 0 0.5rem",paddingTop:i===0?0:"1.5rem",borderTop:i===0?"none":"1px solid #c8b89a"}}>{s.heading}</h3>
                    <p style={{margin:"0 0 1rem"}}>{s.content}</p>
                  </div>
                ))}
              </div>

              <div>
                {[
                  {title:"Risk Assessment", content: (
                    <div>
                      <span style={{fontFamily:"monospace",fontSize:"0.55rem",letterSpacing:"0.1em",textTransform:"uppercase",padding:"0.2rem 0.5rem",border:"1px solid currentColor",display:"inline-block",marginBottom:"0.5rem",color:brief.riskLevel==="HIGH"?"#8b1a1a":brief.riskLevel==="LOW"?"#1a5c3a":"#8b6914"}}>{brief.riskLevel} RISK</span>
                      <p style={{fontSize:"0.82rem",lineHeight:1.6,color:"#6b6355",margin:0}}>{brief.riskRationale}</p>
                    </div>
                  )},
                  {title:"Key Risks", content: (brief.keyRisks||[]).map((r,i)=>(
                    <div key={i} style={{display:"flex",gap:"0.5rem",padding:"0.35rem 0",borderBottom:i<(brief.keyRisks.length-1)?"1px dotted #c8b89a":"none",fontSize:"0.83rem",lineHeight:1.5}}>
                      <span style={{color:"#8b1a1a",fontWeight:700,flexShrink:0}}>◆</span>{r}
                    </div>
                  ))},
                  {title:"Watchlist", content: (brief.watchlist||[]).map((w,i)=>(
                    <div key={i} style={{display:"flex",gap:"0.5rem",padding:"0.35rem 0",borderBottom:i<(brief.watchlist.length-1)?"1px dotted #c8b89a":"none",fontSize:"0.83rem",lineHeight:1.5}}>
                      <span style={{color:"#8b1a1a",fontWeight:700,flexShrink:0}}>→</span>{w}
                    </div>
                  ))}
                ].map(({title,content})=>(
                  <div key={title} style={{background:"#ede8dc",border:"1px solid #c8b89a",borderTop:"3px solid #0d0d0d",padding:"1rem",marginBottom:"1rem"}}>
                    <div style={{fontFamily:"monospace",fontSize:"0.52rem",letterSpacing:"0.2em",textTransform:"uppercase",color:"#6b6355",marginBottom:"0.6rem",paddingBottom:"0.5rem",borderBottom:"1px solid #c8b89a"}}>{title}</div>
                    {content}
                  </div>
                ))}
              </div>
            </div>

            <div style={{marginTop:"2rem",paddingTop:"1.2rem",borderTop:"1px solid #c8b89a",display:"flex",gap:"1rem"}}>
              <button onClick={()=>setBrief(null)} style={{background:"none",border:"1px solid #0d0d0d",padding:"0.5rem 1.2rem",fontFamily:"monospace",fontSize:"0.58rem",letterSpacing:"0.2em",textTransform:"uppercase",cursor:"pointer"}}>← New Brief</button>
              <button onClick={()=>openInTab(brief, today)} style={{background:"#0d0d0d",color:"#f4f0e8",border:"none",padding:"0.5rem 1.2rem",fontFamily:"monospace",fontSize:"0.58rem",letterSpacing:"0.2em",textTransform:"uppercase",cursor:"pointer"}}>↗ Open & Print</button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
