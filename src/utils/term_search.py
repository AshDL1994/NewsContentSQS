import requests
from src.utils.key import the_key
from src.utils.article_content import get_guard_content
import pprint
from datetime import datetime


def article_search(search_term, date=None):

    try:
        if date == None:

            response = requests.get(f"https://content.guardianapis.com/search?q={search_term}&tags?type=article&api-key={the_key}")

        else:

            # Original date string
            original_date = str(date)

            # Convert to datetime object
            date_obj = datetime.strptime(original_date, "%d%m%Y")

            # Convert to desired format
            formatted_date = date_obj.strftime("%Y-%m-%d")

            response = requests.get(f"https://content.guardianapis.com/search?q={search_term}&tags?type=article&from-date={formatted_date}&api-key={the_key}")    
        
        news = response.json()
    
        ten_articles = news['response']['results']
    
        normal_ten_articles = [{"webPublicationDate":result["webPublicationDate"], "webTitle" : result['webTitle'],"webUrl" : result["webUrl"], "Preview" : get_guard_content(result["webUrl"])} for result in ten_articles]
        
        return normal_ten_articles
    
    except Exception as e:
        print(f"the following error occured: {e}")
        return ["Articles could not be retrieved"]
    
    #else:

    #    return "ok this is weird"

#debates = article_search("AI", "01032025")
#pprint.pprint(debates)
# use pprint for the cli potentially