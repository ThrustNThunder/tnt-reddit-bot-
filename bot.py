"""
Thrust N Thunder — Reddit Bot
Posts new video reviews to relevant subreddits and monitors comments.

Usage:
    python bot.py post --title "Video Title" --url "https://youtu.be/..." --video-id "zRHLKrFD1n0"
    python bot.py monitor
"""

import praw
import argparse
import json
import os
from datetime import datetime

# --- Config ---
REDDIT_CLIENT_ID = os.environ.get("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.environ.get("REDDIT_CLIENT_SECRET")
REDDIT_USERNAME = "ThrustNThunder"
REDDIT_PASSWORD = os.environ.get("REDDIT_PASSWORD")
USER_AGENT = "ThrustNThunder Bot v1.0 by u/ThrustNThunder"

# Subreddits and post templates per video type
SUBREDDITS = {
    "starlink": {
        "subs": ["Starlink", "boondocking", "vandwellers", "overlanding", "GoRVing", "camping", "SolarDIY", "boating", "sailing", "Liveaboard", "fishing"],
        "flair_keywords": ["Review", "Hardware", "Discussion", "Gear"]
    }
}

POST_TEMPLATES = {
    "starlink_power": {
        "r/Starlink": {
            "title": "Tested the {product} for off-grid Starlink power — here's what I found",
            "body": (
                "Been running Starlink off-grid for a while and finally got my hands on the {product} "
                "to see if it's actually worth it for field use. Put together a full review covering "
                "real-world performance, battery life, and whether it makes sense as a dedicated Starlink "
                "power solution. If you're trying to run Starlink off battery without a full solar setup, "
                "this might be relevant.\n\nVideo here if anyone's interested: {url}\n\nHappy to answer questions in the comments."
            )
        },
        "r/boondocking": {
            "title": "{product} review — worth it for keeping Starlink running off-grid?",
            "body": (
                "Just posted a full hands-on review of the {product}. Been boondocking and testing gear "
                "for a while now and this one caught my attention as a dedicated power solution for Starlink. "
                "Covers real performance numbers, not just spec sheet claims.\n\nFull review: {url}\n\n"
                "Anyone else running this or something similar for off-grid connectivity?"
            )
        },
        "r/vandwellers": {
            "title": "Reviewed the {product} for van life Starlink power — honest take",
            "body": (
                "If you're running Starlink in a van or truck build, power management is always the headache. "
                "Reviewed the {product} to see if it actually solves that problem or just adds another gadget "
                "to the pile. Honest review, no fluff.\n\nCheck it out: {url}\n\n"
                "What are you all using to power Starlink on the road?"
            )
        },
        "r/overlanding": {
            "title": "Off-grid Starlink power review — {product} real world test",
            "body": (
                "Connectivity in the field is critical and Starlink changed the game — but power is still "
                "the bottleneck. Reviewed the {product} specifically for overlanding/off-grid use cases. "
                "Real world numbers, not marketing specs.\n\nFull review: {url}\n\n"
                "Curious what setups you all are running out there."
            )
        }
    }
}


def get_reddit():
    return praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        username=REDDIT_USERNAME,
        password=REDDIT_PASSWORD,
        user_agent=USER_AGENT
    )


def post_video(title, url, product, template_key="starlink_power", dry_run=False):
    reddit = get_reddit()
    results = []

    templates = POST_TEMPLATES.get(template_key, {})
    for subreddit_name, template in templates.items():
        sub_clean = subreddit_name.replace("r/", "")
        post_title = template["title"].format(product=product, url=url)
        post_body = template["body"].format(product=product, url=url)

        if dry_run:
            print(f"\n[DRY RUN] Would post to r/{sub_clean}:")
            print(f"  Title: {post_title}")
            print(f"  Body: {post_body[:100]}...")
            results.append({"subreddit": sub_clean, "status": "dry_run"})
            continue

        try:
            subreddit = reddit.subreddit(sub_clean)
            submission = subreddit.submit(post_title, selftext=post_body)
            print(f"✅ Posted to r/{sub_clean}: {submission.url}")
            results.append({"subreddit": sub_clean, "status": "success", "url": submission.url})
        except Exception as e:
            print(f"❌ Failed to post to r/{sub_clean}: {e}")
            results.append({"subreddit": sub_clean, "status": "error", "error": str(e)})

    return results


def monitor_comments(limit=10):
    reddit = get_reddit()
    print(f"\n📬 Recent comments on u/ThrustNThunder posts:\n")
    for comment in reddit.redditor(REDDIT_USERNAME).comments.new(limit=limit):
        print(f"  [{comment.subreddit}] {comment.body[:100]}...")
        print(f"  Score: {comment.score} | {datetime.fromtimestamp(comment.created_utc)}\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Thrust N Thunder Reddit Bot")
    subparsers = parser.add_subparsers(dest="command")

    post_parser = subparsers.add_parser("post", help="Post a new video")
    post_parser.add_argument("--title", required=True)
    post_parser.add_argument("--url", required=True)
    post_parser.add_argument("--product", required=True, help="Product name e.g. 'PeakDo LinkPower 2'")
    post_parser.add_argument("--template", default="starlink_power")
    post_parser.add_argument("--dry-run", action="store_true")

    monitor_parser = subparsers.add_parser("monitor", help="Monitor recent comments")
    monitor_parser.add_argument("--limit", type=int, default=10)

    args = parser.parse_args()

    if args.command == "post":
        post_video(args.title, args.url, args.product, args.template, args.dry_run)
    elif args.command == "monitor":
        monitor_comments(args.limit)
    else:
        parser.print_help()
