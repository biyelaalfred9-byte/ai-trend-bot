import os
import requests
import google.generativeai as genai

# Setup Gemini API
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

def get_hacker_news():
    print("Fetching Hacker News...")
    top_ids = requests.get("https://hacker-news.firebaseio.com/v0/topstories.json").json()[:10]
    titles = []
    for story_id in top_ids:
        item = requests.get(f"https://hacker-news.firebaseio.com/v0/item/{story_id}.json").json()
        if 'title' in item:
            titles.append(item['title'])
    return titles

def get_reddit_trends():
    print("Fetching Reddit...")
    headers = {'User-Agent': 'TrendBot/1.0'}
    response = requests.get("https://www.reddit.com/r/artificial/hot.json?limit=10", headers=headers)
    posts = response.json()['data']['children']
    return [post['data']['title'] for post in posts]

def generate_trends_report(hn_titles, reddit_titles):
    print("Asking Gemini to analyze trends...")
    prompt = f"""
    You are an expert AI trend forecaster. Here are the top posts from Hacker News and Reddit's r/artificial today:
    
    Hacker News: {hn_titles}
    Reddit: {reddit_titles}
    
    Based on this data, identify the top 3 emerging AI trends. 
    For each trend, provide:
    1. The name of the trend
    2. A 1-paragraph summary of why it's trending
    3. One actionable content idea (e.g., a YouTube video idea, a blog post title, or a tweet thread)
    
    Format the output in clean Markdown.
    """
    
    response = model.generate_content(prompt)
    
    # Save to markdown file
    with open("trends.md", "w") as f:
        f.write(response.text)
    print("Report saved to trends.md!")

if __name__ == "__main__":
    hn = get_hacker_news()
    reddit = get_reddit_trends()
    generate_trends_report(hn, reddit)
