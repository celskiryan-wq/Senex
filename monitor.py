import feedparser
import re
import anthropic
import json
import requests
from datetime import datetime

import os
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

FEEDS = [
    "https://feeds.bbci.co.uk/news/world/rss.xml",
    "https://feeds.bbci.co.uk/news/business/rss.xml",
    "https://rss.politico.com/politics-news.xml",
]

FILTER_PROMPT = """You are a GPC intelligence analyst. Review this news story and determine if it is worth a full intelligence brief.

A story is worth flagging if it meets ALL of these criteria:
1. Directly involves the US, China, Russia, or their proxies
2. Affects a strategically significant domain: military posture, technology, energy, trade, or diplomatic alignment
3. Is a genuinely new development, not a continuation of something already well covered
4. Has plausible market or economic consequences

Story headline: {headline}
Story summary: {summary}

Respond with JSON only, no other text:
{{"flag": true or false, "reason": "one sentence explanation", "affected_markets": ["list", "of", "markets"]}}"""

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

def check_feeds():
    flagged = []
    
    for feed_url in FEEDS:
        print(f"Checking {feed_url}...")
        try:
            response = requests.get(feed_url, headers=HEADERS, timeout=10)
            feed = feedparser.parse(response.content)
            
            for entry in feed.entries[:10]:
                headline = entry.get("title", "")
                summary = entry.get("summary", "")[:500]
                
                if not headline:
                    continue
                
                print(f"  Evaluating: {headline[:60]}...")
                
                result = client.messages.create(
                    model="claude-haiku-4-5-20251001",
                    max_tokens=200,
                    messages=[{
                        "role": "user",
                        "content": FILTER_PROMPT.format(headline=headline, summary=summary)
                    }]
                )
                
                raw = result.content[0].text.strip()
                match = re.search(r'\{.*\}', raw, re.DOTALL)
                if not match:
                    continue
                data = json.loads(match.group())
                
                if data["flag"]:
                    flagged.append({
                        "headline": headline,
                        "summary": summary,
                        "reason": data["reason"],
                        "affected_markets": data["affected_markets"],
                        "url": entry.get("link", ""),
                        "timestamp": datetime.now().isoformat()
                    })
                    print(f"  FLAG: {headline[:60]}")
                    
        except Exception as e:
            print(f"  Error with {feed_url}: {e}")
    
    return flagged

if __name__ == "__main__":
    print("Senex Monitor Agent running...\n")
    flagged_stories = check_feeds()
    print(f"\n{'='*50}")
    print(f"{len(flagged_stories)} stories flagged for briefing:")
    for story in flagged_stories:
        print(f"\n• {story['headline']}")
        print(f"  Why: {story['reason']}")
        print(f"  Markets: {', '.join(story['affected_markets'])}")
        print(f"  URL: {story['url']}")