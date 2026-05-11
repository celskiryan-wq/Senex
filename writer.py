import anthropic
import json
import re
from datetime import datetime

import os
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

WRITER_PROMPT = """You are a senior intelligence analyst at Senex, a geopolitical market intelligence platform. Using the research package below, write a complete intelligence brief.

RESEARCH PACKAGE:
{research}

Write the brief in this exact JSON structure, no other text:
{{
  "kicker": "Category label in caps e.g. TECHNOLOGY COMPETITION — US-CHINA",
  "headline": "Sharp declarative headline, max 12 words, takes a clear position",
  "deck": "One sentence that captures the central analytical tension, 25-35 words",
  "marketData": [
    {{"label": "Asset or indicator name", "value": "Current level or status", "change": "Directional impact and why", "direction": "up or down or neutral"}},
    {{"label": "Asset or indicator name", "value": "Current level or status", "change": "Directional impact and why", "direction": "up or down or neutral"}},
    {{"label": "Asset or indicator name", "value": "Current level or status", "change": "Directional impact and why", "direction": "up or down or neutral"}},
    {{"label": "Asset or indicator name", "value": "Current level or status", "change": "Directional impact and why", "direction": "up or down or neutral"}}
  ],
  "sections": [
    {{"heading": "The Situation", "content": "2-3 sentences establishing what happened and why it matters in GPC context"}},
    {{"heading": "Market Implications", "content": "2-3 sentences on specific, causal market impacts — name the assets and explain the mechanism"}},
    {{"heading": "Historical Context", "content": "2-3 sentences placing this in historical perspective using the precedent identified"}},
    {{"heading": "Analytical Assessment", "content": "2-3 sentences stating clearly where this leads — take a position, don't hedge"}},
    {{"heading": "What To Watch", "content": "2-3 sentences on the specific indicators that will confirm or challenge this assessment"}}
  ],
  "keyRisks": [
    "Specific risk statement 1",
    "Specific risk statement 2", 
    "Specific risk statement 3"
  ],
  "watchlist": [
    "Specific asset or indicator 1",
    "Specific asset or indicator 2",
    "Specific asset or indicator 3"
  ],
  "riskLevel": "HIGH",
  "riskRationale": "One sentence explaining the risk rating"
}}

Rules:
- Every brief must explicitly name the GPC competitive domain affected
- The analytical assessment must address the long-term trajectory of the competition, not just the immediate event
- Market data must have explicit causal mechanisms — never just a direction
- The brief must take a clear falsifiable position
- Write for think tank researchers and policy professionals who understand GPC frameworks
- No hedging language like 'could potentially' or 'might possibly'
- The GPC implications must be in the first section, not buried
- Distinguish between tactical moves and structural shifts explicitly"""

def write_brief(research_package):
    print(f"Writing brief: {research_package['headline'][:60]}...")
    
    result = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=3000,
        messages=[{
            "role": "user",
            "content": WRITER_PROMPT.format(
                research=json.dumps(research_package, indent=2)
            )
        }]
    )
    
    raw = result.content[0].text.strip()
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not match:
        print("Could not parse brief output")
        return None
    
    brief = json.loads(match.group())
    brief["source_url"] = research_package.get("url", "")
    brief["timestamp"] = datetime.now().isoformat()
    
    print(f"  Done. Headline: {brief.get('headline', '')}")
    return brief

if __name__ == "__main__":
    # Use the research package from researcher.py output
    test_research = {
        "headline": "White House memo claims mass AI theft by Chinese firms",
        "summary": "A White House memo alleges that Chinese companies have been systematically stealing artificial intelligence technology and intellectual property from US firms, escalating technology competition concerns.",
        "background": "US-China technology competition has intensified since at least 2017, when the Trump administration began formally identifying China's industrial espionage and IP theft as a national security threat, culminating in the 2018-2019 trade war and targeted restrictions on firms like Huawei and ZTE. The Biden administration accelerated this posture with sweeping semiconductor export controls in October 2022, and the CHIPS Act was passed specifically to onshore critical technology production. AI has emerged as the defining frontier of this competition.",
        "gpc_angle": "This memo represents a direct escalation in the US government's framing of AI not merely as commercial intellectual property but as a great power competition asset, analogous to nuclear or signals intelligence technology.",
        "key_actors": ["White House NSC", "Chinese Ministry of State Security", "US Department of Commerce", "NVIDIA", "OpenAI", "Google DeepMind", "TSMC"],
        "market_analysis": {
            "primary_impacts": [
                "AI software companies facing increased security scrutiny and compliance costs",
                "Semiconductor firms anticipating expanded export restrictions",
                "US-listed Chinese technology stocks facing delisting and sanctions risk"
            ],
            "secondary_impacts": [
                "Cybersecurity sector tailwind",
                "Cloud infrastructure providers facing pressure to restrict Chinese customer access",
                "Venture capital chilling effect on US-China co-investment"
            ],
            "timeframe": "Immediate market volatility within days; structural impacts over 6-18 months"
        },
        "historical_precedent": "The 2014 DOJ indictment of five PLA Unit 61398 officers established the template of public attribution as deterrence, but produced limited behavioral change while significantly escalating diplomatic friction and prompting retaliatory Chinese cyber operations.",
        "analytical_position": "This memo is best understood as a deliberate policy instrument designed to create political justification for the next tranche of AI-specific export controls, treating frontier AI models under a classification framework similar to dual-use military technology.",
        "risk_level": "HIGH",
        "risk_rationale": "White House-level attribution combined with AI's status as the defining GPC technology creates high probability of material near-term policy action with broad market consequences.",
        "watchlist": ["BIS export control updates", "NVIDIA China revenue guidance", "CFIUS rejection rates", "Chinese retaliation against US tech firms", "KWEB ETF performance"],
        "brief_angle": "AI intellectual property is being reclassified from commercial asset to national security asset, making structured US-China AI decoupling an accelerating certainty.",
        "url": "https://www.bbc.com/news/articles/cpqxgxx9nrqo"
    }
    
    print("Senex Writer Agent running...\n")
    brief = write_brief(test_research)
    
    if brief:
        print("\n" + "="*50)
        print("BRIEF COMPLETE:")
        print("="*50)
        print(json.dumps(brief, indent=2))