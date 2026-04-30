import anthropic
import json
import re
from datetime import datetime

import os
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

EDITOR_PROMPT = """You are the editorial director of Senex, a geopolitical market intelligence platform read by think tank researchers, policy professionals, and institutional investors. 

You are reviewing a draft intelligence brief before publication. Your job is to assess quality and either approve it or return it with specific edits.

DRAFT BRIEF:
{brief}

Evaluate the brief against these standards:
1. HEADLINE — Does it take a clear analytical position? Is it declarative not descriptive?
2. DECK — Does it capture the central tension in 25-35 words? Is it specific not generic?
3. MARKET DATA — Does each entry have an explicit causal mechanism? Are the directions justified?
4. SECTIONS — Does each section add distinct value? Does the analytical assessment commit to a position?
5. KEY RISKS — Are they specific and differentiated, not just variations of the same risk?
6. OVERALL — Would a senior CSIS fellow or institutional risk analyst find this credible and useful?

Respond in JSON only, no other text:
{{
  "approved": true or false,
  "quality_score": 1-10,
  "editorial_notes": {{
    "headline": "assessment of headline quality",
    "deck": "assessment of deck quality", 
    "market_data": "assessment of market data quality",
    "analysis": "assessment of analytical rigor",
    "overall": "overall editorial assessment"
  }},
  "required_changes": ["list of specific changes required if not approved, empty if approved"],
  "publish_recommendation": "PUBLISH NOW or REVISE FIRST or SPIKE",
  "editor_note": "One sentence summary for the editorial record"
}}"""

def edit_brief(brief):
    print(f"Editing: {brief.get('headline', '')[:60]}...")
    
    result = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1500,
        messages=[{
            "role": "user",
            "content": EDITOR_PROMPT.format(
                brief=json.dumps(brief, indent=2)
            )
        }]
    )
    
    raw = result.content[0].text.strip()
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not match:
        print("Could not parse editorial review")
        return None
    
    review = json.loads(match.group())
    
    print(f"  Quality score: {review.get('quality_score', 'N/A')}/10")
    print(f"  Decision: {review.get('publish_recommendation', 'N/A')}")
    print(f"  Note: {review.get('editor_note', '')}")
    
    return review

if __name__ == "__main__":
    # Use the brief from writer.py output
    test_brief = {
        "kicker": "TECHNOLOGY COMPETITION — US-CHINA",
        "headline": "White House Reframes AI Theft as National Security Crisis, Decoupling Accelerates",
        "deck": "By publicly attributing systematic AI IP theft to Chinese state-linked actors, the White House is constructing the legal and political architecture for the most sweeping technology export controls since October 2022.",
        "marketData": [
            {"label": "NVIDIA (NVDA) — Indicative", "value": "Elevated restriction risk on China-facing SKUs", "change": "Down pressure: BIS classification of frontier AI as dual-use technology directly threatens NVIDIA's China revenue segment", "direction": "down"},
            {"label": "KWEB ETF — Indicative", "value": "High sanctions and delisting exposure", "change": "Down pressure: White House attribution memo increases probability of targeted sanctions and accelerated PCAOB delisting", "direction": "down"},
            {"label": "US Cybersecurity Sector — Indicative", "value": "Structural tailwind confirmed", "change": "Up pressure: Government-level theft attribution mandates enterprise AI security upgrades", "direction": "up"},
            {"label": "US-China VC Co-Investment — Indicative", "value": "Near-freeze conditions", "change": "Down pressure: CFIUS scrutiny expansion causes immediate capital withdrawal from dual-flag AI ventures", "direction": "down"}
        ],
        "sections": [
            {"heading": "The Situation", "content": "A White House NSC memo has formally alleged that Chinese firms, operating with implicit Ministry of State Security coordination, have engaged in systematic theft of frontier AI intellectual property from US laboratories and technology companies including OpenAI and Google DeepMind. This is not a law enforcement document — it is a political instrument, and its elevation to White House level signals that frontier AI is now being governed under the same national security logic that produced semiconductor export controls in October 2022. The memo reframes AI model weights, training methodologies, and architectural innovations as assets equivalent in strategic sensitivity to dual-use military technology, creating the doctrinal basis for an entirely new classification and control regime."},
            {"heading": "Market Implications", "content": "NVIDIA faces the most direct near-term exposure: BIS is likely to expand restrictions on H20 and any successor China-compliant chips under a dual-use AI framing, eliminating the regulatory arbitrage that currently sustains NVIDIA's China data center business. US-listed Chinese technology stocks face compounding pressure as the memo provides Congressional ammunition for accelerating both PCAOB enforcement and targeted sectoral sanctions, making KWEB a high-risk vehicle in the immediate 30-90 day window. The cybersecurity sector receives a durable structural tailwind as federal contracting requirements and private sector liability exposure force enterprise-wide AI IP protection investment."},
            {"heading": "Historical Context", "content": "The 2014 DOJ indictment of five PLA Unit 61398 officers established the US template of public attribution as deterrence, but produced no measurable reduction in Chinese cyber operations while triggering significant diplomatic retaliation. The more instructive precedent is the October 2022 semiconductor export control package, which demonstrated that the current administration is willing to impose economically costly unilateral restrictions when the national security framing is sufficiently established — and the White House memo is performing exactly that framing function for AI."},
            {"heading": "Analytical Assessment", "content": "This memo is the predicate document for the next major tranche of AI-specific export controls, and those controls will arrive within the 6-12 month window with or without allied coordination. The classification of frontier AI models as national security assets is now institutionally locked in at the White House level, meaning the policy direction is irreversible under any plausible near-term political scenario. Structured US-China AI decoupling is no longer a risk to be monitored — it is the baseline, and markets that have not priced this as a permanent structural condition are mispriced."},
            {"heading": "What To Watch", "content": "The Bureau of Industry and Security's regulatory docket is the primary leading indicator: any new AI-specific entity list additions or proposed rulemaking on model weight controls will confirm the memo has moved from political signal to operational policy. NVIDIA's next earnings guidance on China revenue will reveal whether the company's internal risk assessment has shifted. Chinese government statements targeting US technology firms will signal whether Beijing has chosen economic retaliation as its primary response instrument."}
        ],
        "keyRisks": [
            "BIS implements emergency AI export controls ahead of notice-and-comment timeline, creating immediate compliance discontinuity for NVIDIA and cloud providers",
            "China retaliates with targeted operational disruptions against US technology firms on Chinese soil, including regulatory harassment of Apple supply chain",
            "Allied governments decline to coordinate on AI export controls, fragmenting enforcement and creating third-country routing that undermines the control regime"
        ],
        "watchlist": [
            "BIS entity list updates and AI-specific export control rulemaking",
            "NVIDIA China revenue guidance and H20 chip shipment data",
            "CFIUS rejection rates for US-China technology transactions"
        ],
        "riskLevel": "HIGH",
        "riskRationale": "White House-level attribution combined with institutional willingness to impose unilateral technology controls creates high-confidence expectation of material near-term policy action.",
        "source_url": "https://www.bbc.com/news/articles/cpqxgxx9nrqo",
        "timestamp": "2026-04-26T20:10:27.306061"
    }
    
    print("Senex Editor Agent running...\n")
    review = edit_brief(test_brief)
    
    if review:
        print("\n" + "="*50)
        print("EDITORIAL REVIEW COMPLETE:")
        print("="*50)
        print(json.dumps(review, indent=2))