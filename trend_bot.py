import os
import requests
import xml.etree.ElementTree as ET
import google.generativeai as genai

# Setup Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
# Using the current stable model name to fix the 404 error
model = genai.GenerativeModel('gemini-2.5-flash')

def get_hacker_news():
    print("Fetching Hacker News...")
    try:
        top_ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()[:10]
        titles = []
        for story_id in top_ids:
            item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json").json()
            if 'title' in item:
                titles.append(item['title'])
        return titles
    except Exception as e:
        print(f"Hacker News failed: {e}")
        return []

def get_google_news():
    print("Fetching Google News AI trends...")
    try:
        url = "https://news.google.com/rss/search?q=artificial+intelligence&hl=en-US&gl=US&ceid=US:en"
        response = requests.get(url)
        root = ET.fromstring(response.content)
        titles = [item.find('title').text for item in root.findall('.//item')[:10]]
        return titles
    except Exception as e:
        print(f"Google News failed: {e}")
        return []

def generate_trends_report(hn_titles, google_titles):
    print("Asking Gemini to analyze trends...")
    if not hn_titles and not google_titles:
        print("No data found to analyze.")
        return
        
    prompt = f"""
    You are an expert AI trend forecaster. Here are the top posts from Hacker News and Google News today:
    
    Hacker News: {hn_titles}
    Google News: {google_titles}
    
    Based on this data, identify the top 3 emerging AI trends. 
    For each trend, provide:
    1. The name of the trend
    2. A 1-paragraph summary of why it's trending
    3. One actionable content idea (e.g., a YouTube video idea, a blog post title, or a tweet thread)
    
    Format the output in clean Markdown.
    """
    
    response = model.generate_content(prompt)
    
    with open("trends.md", "w") as f:
        f.write(response.text)
    print("Report saved to trends.md!")

if __name__ == "__main__":
    hn = get_hacker_news()
    google = get_google_news()
    generate_trends_report(hn, google)
