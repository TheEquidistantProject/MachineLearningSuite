import openai
import pinecone
import json
import pandas as pd
from tqdm import tqdm
import time
import datetime

from pymongo.mongo_client import MongoClient

uri = "mongodb+srv://muthu:adi123@cluster0.rgzozbh.mongodb.net/?retryWrites=true&w=majority"
# Create a new client and connect to the server
client = MongoClient(uri)

# initialize connection to pinecone (get API key at app.pinecone.io)
pinecone.init(
    api_key="3d4d50e3-d000-4c99-98ec-de166860b1df",
    environment="gcp-starter"  # find next to API key in console
)

index = pinecone.Index('openai')

openai.api_key = ""

MODEL = "text-embedding-ada-002"


while True:
    with open('cnn.json', 'r') as f:
        data = json.load(f)

    # Convert data to pandas DataFrame
    data_df = pd.DataFrame(data)

    batch_size = 1# process everything in batches of 16
    for i in tqdm(range(0, len(data_df), batch_size)):
        # set end position of batch
        i_end = min(i + batch_size, len(data_df))
        # get batch of lines and IDs
        lines_batch = data_df.iloc[i: i_end]
        ids_batch = [str(n) for n in range(i, i_end)]
        # create embeddings
        res = openai.Embedding.create(input=list(lines_batch["content"]), engine=MODEL)
        embeds = [record['embedding'] for record in res['data']]
        res = index.query([embeds], top_k=1, include_metadata=True)
        for match in res['matches']:
            if match['score'] > 0.85:
                generate = openai.Completion.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt = "Generate an unbiased fact-only news article with only this information:" + "\n\nContent: " + match['metadata']['content'] + "\n\n + lines_batch['content'] + \n\n",
                    temperature=0.3,
                    max_tokens=1024,
                    top_p=1,
                )
                news_article = generate['choices'][0]['text']
                generate = openai.Completion.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt = "Choose only between these Tags ('World News', 'National News', 'Politics', 'Business', 'Technology','Science', 'Health', 'Environment', 'Entertainment', 'Sports') for this article:\n\n" + news_article + "\n\n Seperate it by commas",
                    temperature=0.2,
                    max_tokens=40,
                    top_p=1,
                )
                hashtags = generate['choices'][0]['text']
                generate = openai.Completion.create(
                    model="gpt-3.5-turbo-instruct",
                    prompt = "Generate a plain uninspiring Title for this article:\n\n" + news_article + "\n\n",
                    temperature=0.3,
                    max_tokens=100,
                    top_p=1,
                )
                title = generate['choices'][0]['text']
                client["news"]["Articles"].insert_one({"title": title, "urlToImage": [match['metadata']['urlToImage'], lines_batch["urlToImage"].iloc[0]], "news_article": news_article, "hashtags": hashtags, "date": datetime.date.today().strftime('%Y-%m-%d')})
                break;


                



        




