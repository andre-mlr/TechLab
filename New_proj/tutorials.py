import requests
from bs4 import BeautifulSoup

def search_tutorial(tool_name, api_key):
    query = f"{tool_name} tutorial"
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&key={api_key}&maxResults=5"
    
    response = requests.get(url)
    if response.status_code != 200:
        return []

    data = response.json()
    links = []
    for item in data['items']:
        video_id = item['id']['videoId']
        video_url = f"https://www.youtube.com/watch?v={video_id}"
        links.append(video_url)
    
    return links

def get_tutorial(tool_name, api_key):
    tutorials = search_tutorial(tool_name, api_key)
    if not tutorials:
        return f"Desculpe, não consegui encontrar tutoriais sobre {tool_name}."

    response = f"Aqui estão alguns tutoriais sobre {tool_name}:\n"
    for tutorial in tutorials:
        response += f"- {tutorial}\n"
    return response
