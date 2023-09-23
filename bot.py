import requests
import json
from bs4 import BeautifulSoup
import time

def scrape_cnn_article(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    # Check for a valid response (HTTP Status Code 200)
    response.raise_for_status()
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Assume the article text is contained within <div> elements with a class of 'zn-body__paragraph'
    # (This is a simplification and may not work for all CNN articles)
    return json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))

# Example usage:
# article_text = scrape_cnn_article('https://www.cnn.com/2023/09/22/us/some-article/index.html')

def cnn():
    # Download xml file to parse for article urls
    url = "https://www.cnn.com/sitemaps/cnn/news.xml"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = [loc.text for loc in soup.find_all("loc")]
    # print(urls)
    articles = []
    for url in urls:
        try:
            articles.append(scrape_cnn_article(url))
        except:
            continue
    return articles

def scrape_fox_article(url):
    # Send an HTTP GET request to the URL
    response = requests.get(url)
    # Check for a valid response (HTTP Status Code 200)
    response.raise_for_status()
    
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Assume the article text is contained within <div> elements with a class of 'zn-body__paragraph'
    # (This is a simplification and may not work for all CNN articles)
    return json.loads("".join(soup.find("script", {"type":"application/ld+json"}).contents))

# Example usage:
# article_text = scrape_cnn_article('https://www.cnn.com/2023/09/22/us/some-article/index.html')
#print(scrape_fox_article("https://www.foxnews.com/us/judge-rule-whether-9-11-defendant-deemed-psychotic-delusional-cia-torture-stand-trial-report")["articleBody"])

def fox():
    # Download xml file to parse for article urls
    url = "https://www.foxnews.com/sitemap.xml?type=news"
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, 'html.parser')
    urls = [loc.text for loc in soup.find_all("loc")]
    # print(urls)
    articles = []
    for url in urls:
        try:
            articles.append(scrape_fox_article(url))
        except:
            continue
    return articles


if __name__ == "__main__":
    done = 0
    while True:
        fox_list = []
        cnn_list = []
        lst = fox()
        for i in lst:
            try:
                urlToImage = i["image"]["url"]
                title = i["headline"]
                content = i["articleBody"]
                source = i["publisher"]["name"]
                publishedAt = i["datePublished"]
                fox_list.append({"urlToImage": urlToImage, "title": title, "content": content, "source": source, "publishedAt": publishedAt})
            except:
                continue
        lst = cnn()
        for i in lst:
            try:
                urlToImage = i["image"][0]["contentUrl"]
                title = i["headline"]
                content = i["articleBody"]
                source = i["publisher"]["name"]
                publishedAt = i["datePublished"]
                cnn_list.append({"urlToImage": urlToImage, "title": title, "content": content, "source": source, "publishedAt": publishedAt})
            except:
                continue
        print(len(fox_list))
        print(len(cnn_list))
        with open("fox.json", "w") as f:
            json.dump(fox_list, f)
        with open("cnn.json", "w") as f:
            json.dump(cnn_list, f)
        done += 1
        print(f"done {done}")
        time.sleep(60*60*5)


