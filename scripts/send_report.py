import os
import json
import requests

BOT_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

def format_num(n):
    n = n or 0
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n/1_000:.1f}K"
    return str(n)

def load_data():
    with open("dashboard/data.json", "r", encoding="utf-8") as f:
        return json.load(f)

def build_report(data):
    valid = [d for d in data if not d.get("error")]
    errored = [d for d in data if d.get("error")]

    total_posts = len(valid)
    for p in valid:
        p["_views"] = p.get("videoViewCount") or p.get("videoPlayCount") or p.get("likesCount") or 0

    total_views = sum(p["_views"] for p in valid)
    total_comments = sum(p.get("commentsCount") or 0 for p in valid)
    avg_views = round(total_views / total_posts) if total_posts else 0

    top_posts = sorted(valid, key=lambda p: p["_views"], reverse=True)[:3]

    tag_counts = {}
    for p in valid:
        for t in p.get("hashtags") or []:
            tag_counts[t] = tag_counts.get(t, 0) + 1
    top_tags = sorted(tag_counts.items(), key=lambda x: x[1], reverse=True)[:5]

    lines = []
    lines.append("📊 *Bhavin AI Stories — Daily Content Report*")
    lines.append("")
    lines.append(f"Posts tracked: *{total_posts}*")
    lines.append(f"Total views: *{format_num(total_views)}*")
    lines.append(f"Avg views/post: *{format_num(avg_views)}*")
    lines.append(f"Total comments: *{format_num(total_comments)}*")
    lines.append("")
    lines.append("🏆 *Top posts:*")
    for p in top_posts:
        caption = (p.get("caption") or "").replace("\n", " ")[:80]
        lines.append(f"• {format_num(p['_views'])} views — {caption}")
    lines.append("")
    lines.append("🔥 *Top hashtags:*")
    lines.append(" ".join(f"#{t}({c})" for t, c in top_tags))

    if errored:
        lines.append("")
        lines.append(f"⚠️ {len(errored)} account(s) failed to scrape.")

    return "\n".join(lines)

def send_message(text):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    resp = requests.post(url, json={
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "Markdown"
    })
    resp.raise_for_status()
    print("Report sent successfully.")

if __name__ == "__main__":
    data = load_data()
    report = build_report(data)
    send_message(report)
