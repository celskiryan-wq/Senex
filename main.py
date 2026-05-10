import json
import os
from datetime import datetime
from supabase import create_client
from monitor import check_feeds
from researcher import research_story
from writer import write_brief
from editor import edit_brief

# Supabase client
supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)
def save_brief(brief, review):
    """Save approved brief to Supabase and local JSON"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"briefs/brief_{timestamp}.json"
    
    os.makedirs("briefs", exist_ok=True)
    
    output = {
        "brief": brief,
        "editorial_review": review,
        "published_at": datetime.now().isoformat()
    }
    
    with open(filename, "w") as f:
        json.dump(output, f, indent=2)
    
    # Save to Supabase
    try:
        supabase.table("briefs").insert({
            "headline": brief.get("headline", ""),
            "kicker": brief.get("kicker", ""),
            "deck": brief.get("deck", ""),
            "market_data": brief.get("marketData", []),
            "sections": brief.get("sections", []),
            "key_risks": brief.get("keyRisks", []),
            "watchlist": brief.get("watchlist", []),
            "risk_level": brief.get("riskLevel", ""),
            "risk_rationale": brief.get("riskRationale", ""),
            "source_url": brief.get("source_url", ""),
            "quality_score": review.get("quality_score", 0),
            "editor_note": review.get("editor_note", "")
        }).execute()
        print(f"  Saved to Supabase ✓")
    except Exception as e:
        print(f"  Supabase save failed: {e}")
    
    print(f"  Saved to {filename}")
    return filename

def run_pipeline():
    print("=" * 60)
    print("SENEX INTELLIGENCE PIPELINE")
    print(f"Running at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # STEP 1 — MONITOR
    print("\n[1/4] MONITOR — Scanning news feeds...")
    flagged_stories = check_feeds()
    print(f"  {len(flagged_stories)} stories flagged")
    
    if not flagged_stories:
        print("  No stories flagged. Pipeline complete.")
        return
    
    # STEP 2 — RESEARCHER
    print("\n[2/4] RESEARCHER — Building research packages...")
    research_packages = []
    for story in flagged_stories[:2]:  # Cap at 2 briefs per run to manage costs
        package = research_story(story)
        if package:
            research_packages.append(package)
    
    print(f"  {len(research_packages)} research packages complete")
    
    if not research_packages:
        print("  No research packages produced. Pipeline complete.")
        return
    
    # STEP 3 — WRITER
    print("\n[3/4] WRITER — Drafting intelligence briefs...")
    drafts = []
    for package in research_packages:
        brief = write_brief(package)
        if brief:
            drafts.append(brief)
    
    print(f"  {len(drafts)} briefs drafted")
    
    # STEP 4 — EDITOR
    print("\n[4/4] EDITOR — Reviewing briefs...")
    published = []
    for brief in drafts:
        review = edit_brief(brief)
        if review:
            recommendation = review.get("publish_recommendation", "")
            score = review.get("quality_score", 0)
            
            if recommendation == "PUBLISH NOW":
                filename = save_brief(brief, review)
                published.append(filename)
                print(f"  APPROVED ({score}/10): {brief.get('headline', '')[:50]}")
            elif recommendation == "REVISE FIRST":
                print(f"  REVISE ({score}/10): {brief.get('headline', '')[:50]}")
                print(f"  Changes needed: {review.get('required_changes', [])}")
            else:
                print(f"  SPIKED ({score}/10): {brief.get('headline', '')[:50]}")
    
    # SUMMARY
    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print(f"  Stories flagged: {len(flagged_stories)}")
    print(f"  Briefs drafted: {len(drafts)}")
    print(f"  Briefs approved: {len(published)}")
    if published:
        print(f"  Saved to:")
        for f in published:
            print(f"    {f}")
    print("=" * 60)

if __name__ == "__main__":
    run_pipeline()
    
    # Auto-render approved briefs to HTML
    from renderer import render_all_briefs
    render_all_briefs()
