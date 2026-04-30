import anthropic
import requests
import json
import re
from datetime import datetime

import os
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
RESEARCH_PROMPT = """You are a senior GPC intelligence researcher. A story has been flagged for a full intelligence brief. Your job is to produce a comprehensive research package.

FLAGGED STORY:
Headline: {headline}
Summary: {summary}
Affected Markets: {markets}

Produce a research package in JSON format only, no other text:
{{
  "background": "2-3 sentences of essential context and history behind this story",
  "gpc_angle": "How does this connect to US-China or US-Russia great power competition specifically?",
  "key_actors": ["list", "of", "key", "state", "and", "non-state", "actors"],
  "market_analysis": {{
    "primary_impacts": ["most directly affected markets with brief explanation"],
    "secondary_impacts": ["indirectly affected markets"],
    "timeframe": "immediate/short-term/medium-term assessment"
  }},
  "historical_precedent": "Most relevant historical parallel and what it tells us",
  "analytical_position": "Clear directional assessment — what does this mean and where does it lead?",
  "risk_level": "HIGH or MEDIUM or LOW",
  "risk_rationale": "One sentence explaining the risk rating",
  "watchlist": ["specific indicators or assets to monitor closely"],
  "brief_angle": "The single most important analytical point this brief should make"
}}"""

def research_story(flagged_story):
    print(f"Researching: {flagged_story['headline'][:60]}...")
    
    result = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=2000,
        messages=[{
            "role": "user",
            "content": RESEARCH_PROMPT.format(
                headline=flagged_story["headline"],
                summary=flagged_story["summary"],
                markets=", ".join(flagged_story["affected_markets"])
            )
        }]
    )
    
    raw = result.content[0].text.strip()
    match = re.search(r'\{.*\}', raw, re.DOTALL)
    if not match:
        print(f"  Could not parse research for: {flagged_story['headline']}")
        return None
    
    research = json.loads(match.group())
    research["headline"] = flagged_story["headline"]
    research["summary"] = flagged_story["summary"]
    research["url"] = flagged_story["url"]
    research["timestamp"] = datetime.now().isoformat()
    
    print(f"  Done. Risk level: {research.get('risk_level', 'unknown')}")
    print(f"  Angle: {research.get('brief_angle', '')[:80]}...")
    
    return research

def research_all(flagged_stories):
    packages = []
    for story in flagged_stories:
        package = research_story(story)
        if package:
            packages.append(package)
    return packages

if __name__ == "__main__":
    # Test with one of the stories the Monitor flagged
    test_story = {
        "headline": "White House memo claims mass AI theft by Chinese firms",
        "summary": "A White House memo alleges that Chinese companies have been systematically stealing artificial intelligence technology and intellectual property from US firms, escalating technology competition concerns.",
        "affected_markets": ["artificial intelligence", "semiconductor", "software", "technology manufacturing", "US-China trade"],
        "url": "https://www.bbc.com/news/articles/cpqxgxx9nrqo"
    }
    
    print("Senex Researcher Agent running...\n")
    package = research_story(test_story)
    
    if package:
        print("\n" + "="*50)
        print("RESEARCH PACKAGE COMPLETE:")
        print("="*50)
        print(json.dumps(package, indent=2))