import json
import os
from datetime import datetime
from monitor import check_feeds
from researcher import research_story
from writer import write_brief
from editor import edit_brief

def save_brief(brief, review):
    """Save approved brief to a JSON file for now — we'll wire up Beehiiv later"""
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