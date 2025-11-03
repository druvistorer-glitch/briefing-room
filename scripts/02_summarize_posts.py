import os
import json
from pathlib import Path
from transformers import pipeline
from scripts.utils import DAILY_DIR, SUMMARIES_DIR, today_str
from dotenv import load_dotenv

load_dotenv()

# model choice: smallish but decent for CPU
MODEL_NAME = "sshleifer/distilbart-cnn-12-6"

# Create summarizer pipeline (may download model on first run)
summarizer = pipeline("summarization", model=MODEL_NAME)

def make_prompt(post):
    title = post.get("title","")
    text = post.get("selftext","") or ""
    comments = "\n\n".join([c.get("body","") for c in post.get("top_comments", [])])
    longtext = f"Title: {title}\n\nPost: {text}\n\nTop comments:\n{comments}"
    return longtext[:18000]

def summarize_post(post):
    prompt = make_prompt(post)
    try:
        out = summarizer(prompt, max_length=220, min_length=80, do_sample=False)
        summary = out[0]["summary_text"]
    except Exception as e:
        summary = f"Summarization failed: {e}"
    return summary

def run(date=None):
    date = date or today_str()
    infile = DAILY_DIR / f"{date}.json"
    if not infile.exists():
        print("No data for", infile)
        return
    with open(infile, "r", encoding="utf-8") as f:
        posts = json.load(f)

    outdir = SUMMARIES_DIR / date
    outdir.mkdir(parents=True, exist_ok=True)
    for p in posts:
        summ = summarize_post(p)
        md = f"### {p['title']} (r/{p['subreddit']})\n\n**Summary:**\n\n{summ}\n\n**Link:** {p['permalink']}\n\n**Upvotes:** {p['score']}\n"
        outpath = outdir / f"{p['id']}.md"
        with open(outpath, "w", encoding="utf-8") as f:
            f.write(md)
        print("Wrote", outpath)

if __name__ == "__main__":
    run()
