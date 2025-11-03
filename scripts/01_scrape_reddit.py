import praw
import os
from scripts.utils import DAILY_DIR, today_str, save_json
from dotenv import load_dotenv

load_dotenv()

CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
USER_AGENT = os.getenv("REDDIT_USER_AGENT") or "briefing-room-bot/0.1"

if not CLIENT_ID or not CLIENT_SECRET:
    raise EnvironmentError("REDDIT_CLIENT_ID or REDDIT_CLIENT_SECRET not set in environment.")

reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)

SUBREDDITS = [
    "worldnews","news","politics","technology","futurology","mademesmile",
    "memes","AskReddit","science","TrueOffMyChest","WhitePeopleTwitter",
    "murderedbywords","publicfreakout","goodnews","TikTokCringe","Anticonsumption",
    "NoFilterNews","Fauxmoi","clevercomebacks","funny","todayilearned","GenZ",
    "millennials","coolguides","foundsatan","WorkReform","Law","CringeTikToks"
]

MIN_SCORE = 5000  # lower initial threshold to capture more; tune later

def extract_post(post):
    try:
        post.comments.replace_more(limit=0)
    except Exception:
        pass
    top_comments = []
    for c in list(post.comments)[:5]:
        top_comments.append({
            "author": str(getattr(c, "author", None)),
            "body": getattr(c, "body", ""),
            "score": getattr(c, "score", None)
        })
    return {
        "id": post.id,
        "title": post.title,
        "selftext": post.selftext,
        "url": post.url,
        "subreddit": str(post.subreddit),
        "score": post.score,
        "created_utc": int(post.created_utc),
        "permalink": "https://reddit.com" + post.permalink,
        "top_comments": top_comments
    }

def run():
    results = []
    for sub in SUBREDDITS:
        subreddit = reddit.subreddit(sub)
        for submission in subreddit.top(time_filter='day', limit=100):
            if submission.score >= MIN_SCORE:
                results.append(extract_post(submission))
    filename = DAILY_DIR / f"{today_str()}.json"
    save_json(results, filename)
    print(f"Saved {len(results)} posts to {filename}")

if __name__ == "__main__":
    run()
