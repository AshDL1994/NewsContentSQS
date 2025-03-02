import pytest
import requests
from src.utils.article_content import get_guard_content
from bs4 import BeautifulSoup

url1 = "https://www.theguardian.com/technology/2025/jan/14/british-novelists-criticise-government-over-ai-theft"
url2 = "https://www.bbc.co.uk/news/articles/cn7rx05xg2go"

def test_get_guard_content_real_url():
    input_url = url1
    result = get_guard_content(input_url)
    assert isinstance(result,str)
    assert len(result) == 1003

def test_get_guard_content_non_guard_url():
    input_url = url2
    result = get_guard_content(input_url)
    assert isinstance(result,str)
    assert result == "Preview unavaliable"

def test_get_guard_content_not_url():
    input_url = 12345
    result = get_guard_content(input_url)
    assert isinstance(result,str)
    assert result == "The following error occured: Invalid URL '12345': No scheme supplied. Perhaps you meant https://12345?"    