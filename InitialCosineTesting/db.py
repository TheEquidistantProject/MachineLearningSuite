# pip install pandas, openai, scipy, matplotlib, plotly, scikit-learn, numpy

import pandas as pd
import openai
from openai.embeddings_utils import cosine_similarity
from random import choice

openai.api_key = 'sk-...'

class VectorDB():
    def __init__(self) -> None:
        self.left = pd.DataFrame(columns=['id', 'title', 'content', 'source', 'publishedAt', 'urlToImage', 'vector', 'closest_article_id'])
        self.right = pd.DataFrame(columns=['id', 'title', 'content', 'source', 'publishedAt', 'urlToImage', 'vector', 'closest_article_id'])

    def add_left(self, article):
        # get vector
        vector = self.get_vector(article['content'])
        # compare with all right articles and find id of article with highest similarity
        closest_article_id = None
        max_similarity = 0

        for i in range(len(self.right)):
            similarity = cosine_similarity(vector, self.right.iloc[i]['vector'])
            if similarity > max_similarity:
                max_similarity = similarity
                closest_article_id = self.right.iloc[i]['id']
        
        # add to left
        article['vector'] = vector
        article['closest_article_id'] = closest_article_id
        # update right
        if closest_article_id != None:
            self.right[self.right['id'] == closest_article_id]['closest_article_id'] = article['id']

        self.left = pd.concat([self.left, pd.DataFrame(article)])

    def add_right(self, article):
        # get vector
        vector = self.get_vector(article['content'])
        # compare with all left articles and find id of article with highest similarity
        closest_article_id = None
        max_similarity = 0
        for i in range(len(self.left)):
            similarity = cosine_similarity(vector, self.left.iloc[i]['vector'])
            if similarity > max_similarity:
                max_similarity = similarity
                closest_article_id = self.left.iloc[i]['id']
        
        # update left
        if closest_article_id != None:
            self.left[self.left['id'] == closest_article_id]['closest_article_id'] = article['id']
        # add to right
        article['vector'] = vector
        article['closest_article_id'] = closest_article_id

        self.right = pd.concat([self.right, pd.DataFrame(article)])

    def get_vector(self, article):
        response = openai.Embedding.create(
            input=article,
            model="text-embedding-ada-002"
        )
        return [e['embedding'] for e in response['data']]
    
    def get_combined(self, article_id, side=None):
        if side == None:
            side = choice(['left', 'right'])

        if side == 'left':
            article = self.left[self.left['id'] == article_id]
            closest_article_id = int(article['closest_article_id'])
            closest_article = self.right[self.right['id'] == closest_article_id]
        elif side == 'right':
            article = self.right[self.right['id'] == article_id]
            closest_article_id = int(article['closest_article_id'])

            closest_article = self.left[self.left['id'] == closest_article_id]            

        prompt="Below are two articles covering the same topic, go through them and generate a new article combining them and covering both sides:\nArticle 1:\n{}\nArticle 2:\n{}\n\nArticle 3:\n".format(article['content'], closest_article['content'])


        new_content = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=prompt,
            max_tokens=1024,
            temperature=0.5,
        )['choices'][0]['text']

        new_title = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Suggest a good title for this article:\n {new_content}\n\n",
            max_tokens=50,
            temperature=0.5,
        )['choices'][0]['text']

        return {
            'title': new_title,
            'content': new_content,
            'source': article['source']+' and '+closest_article['source'],
            'publishedAt': article['publishedAt'],
            'urlToImage': choice([article['urlToImage'], closest_article['urlToImage']]),
            'categories': self.get_categories(new_content)
        }
    
    def get_categories(self, text):
        # use text to generate comma separated list of categories

        response = openai.Completion.create(
            model="gpt-3.5-turbo-instruct",
            prompt=f"Generate a comma separated list of tags for this article:\nyour options are: World News, National News, Politics, Business, Technology, Science, Health, Environment, Entertainment, Sports\n {text}\n\n",
            max_tokens=10,
            temperature=0.5,
        )['choices'][0]['text']
        print(response)

        return response.strip().split(',')
    
    def get_new_articles(self):
        # see which side has less articles
        if len(self.left) < len(self.right):
            side = 'left'
            db = self.left
        else:
            side = 'right'
            db = self.right

        # get new articles for all of these which have a closest article
        new_articles = []
        temp = db[db['closest_article_id'] != None]
        for i in range(len(temp)):
            article = temp.iloc[i]
            new_articles.append(self.get_combined(article['id'], side=side))
        return new_articles

import json


# ExampleArticle:
# {'urlToImage': 'https://media.cnn.com/api/v1/images/stellar/prod/230923130522-jimmy-rosalynn-carter-file-2018.jpg?c=original',
#  'title': 'Jimmy and Rosalynn Carter visit Georgia festival ahead of former president’s 99th birthday, Carter Center says',
#  'content': 'Former President Jimmy Carter and his wife, Rosalynn, took a ride through the Plains Peanut Festival in Plains, Georgia, on Saturday, the Carter Center said in a social media post.  “Beautiful day for President & Mrs. Carter to enjoy a ride through the Plains Peanut Festival! And just a week before he turns 99. We’re betting peanut butter ice cream is on the menu for lunch! #JimmyCarter99,” the Carter Center said in a tweet sharing a video of the Carters riding in an SUV down a street lined with festival-goers. Jimmy Carter, who turns 99 on October 1, entered hospice care in February. The former president beat brain cancer in 2015 but faced a series of health scares in 2019, and consequentially underwent surgery to remove pressure on his brain. In an interview with People published last month, the Carters’ grandson said, “It’s clear we’re in the final chapter.” Family and caregivers had been the only recent visitors to the Carters’ Plains home, Josh Carter told People.  Josh Carter said his grandmother Rosalynn Carter, who has dementia, is cognizant of her diagnosis. “She still knows who we are, for the most part – that we are family,” he said. Jimmy and Rosalynn Carter have been married for 77 years and are the longest-married presidential couple. Jimmy Carter was born in Plains, Georgia, and grew up in the nearby community of Archery. A peanut farmer and Navy lieutenant before going into politics, the Democrat served one term as governor of Georgia and was president from 1977 to 1981.',
#  'source': 'CNN',
#  'publishedAt': '2023-09-23T18:51:26Z',
#  'id': -3059632832363739956}

def test(n=3):
    with open('../cnn.json', 'r') as f:
        cnn_articles = json.load(f)

    with open('../fox.json', 'r') as f:
        fox_articles = json.load(f)

    test_db = VectorDB()
    for article in cnn_articles[:n]:
        article['id'] = hash(article['title'])
        test_db.add_left(article)

    for article in fox_articles[:n]:
        article['id'] = hash(article['title'])
        test_db.add_right(article)

    return test_db.get_new_articles()

