import os
import requests
import xml.etree.ElementTree as ET
from datetime import datetime

def get_hacker_news():
    print("Fetching Hacker News...")
    try:
        top_ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()[:5]
        titles = []
        for story_id in top_ids:
            item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json").json()
            if 'title' in item:
                titles.append(f"- [{item['title']}]({item.get('url', 'https://news.ycombinator.com/item?id=' + str(story_id))})")
        return titles
    except Exception as e:
        print(f"Hacker News failed: {e}")
        return ["- Hacker News data unavailable today"]

def get_google_news():
    print("Fetching Google News AI trends...")
    try:
        url = "https://news.google.com/rss/search?q=artificial+intelligence&hl=en-US&gl=US&ceid=US:en"
        response = requests.get(url)
        root = ET.fromstring(response.content)
        titles = []
        for item in root.findall('.//item')[:5]:
            title = item.find('title').text
            link = item.find('link').text
            titles.append(f"- [{title}]({link})")
        return titles
    except Exception as e:
        print(f"Google News failed: {e}")
        return ["- Google News data unavailable today"]

def generate_report(hn_titles, google_titles):
    print("Building report...")
    date_str = datetime.now().strftime("%Y-%m-%d")
    
    report = f"""# 🤖 Daily AI Trend Report - {date_str}

## 🔥 Top AI Stories from Hacker News
{chr(10).join(hn_titles)}

## 📰 Top AI Headlines from Google News
{chr(10).join(google_titles)}

---
*Generated automatically by your AI Trend Finder Bot.*
"""
    
    with open("trends.md", "w") as f:
        f.write(report)
    print("Report saved to trends.md!")

if __name__ == "__main__":
    hn = get_hacker_news()
    google = get_google_news()
    generate_report(hn, google)
