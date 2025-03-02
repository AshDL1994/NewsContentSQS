from bs4 import BeautifulSoup
import requests

def get_guard_content(input_url):
    try:    
        response = requests.get(input_url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            article_content = soup.find('div', {'style': '--grid-area:body;'})
            if article_content:
                paragraphs = article_content.find_all('p')
                article_text = "\n".join([para.get_text() for para in paragraphs])
                thousand_chars = article_text[:1000]
                return thousand_chars + "..."
            else:
                return "Preview unavaliable"
        else:
            return "Preview unavaliable"    
    except Exception as e:
        print(f"The following error occured: {e}")
        return f"The following error occured: {e}"
