import openai
import pinecone
from tqdm.auto import tqdm  # this is our progress bar
import pandas as pd
import json
import time

openai.api_key = "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"

MODEL = "text-embedding-ada-002"

res = openai.Embedding.create(
    input=[
        "Sample document text goes here",
        "there will be several phrases in each batch"
    ], engine=MODEL
)

embeds = [record['embedding'] for record in res['data']]

# initialize connection to pinecone (get API key at app.pinecone.io)
pinecone.init(
    api_key="3d4d50e3-d000-4c99-98ec-de166860b1df",
    environment="gcp-starter"  # find next to API key in console
)

# check if 'openai' index already exists (only create index if not)
if 'openai' not in pinecone.list_indexes():
    pinecone.create_index('openai', dimension=len(embeds[0]))
# connect to index
index = pinecone.Index('openai')

while True:
    # Load data from JSON file
    with open('fox.json', 'r') as f:
        data = json.load(f)

    # Convert data to pandas DataFrame
    data_df = pd.DataFrame(data)

    batch_size = 16  # process everything in batches of 16
    for i in tqdm(range(0, len(data_df), batch_size)):
        # set end position of batch
        i_end = min(i + batch_size, len(data_df))
        # get batch of lines and IDs
        lines_batch = data_df.iloc[i: i + batch_size]
        ids_batch = [str(n) for n in range(i, i_end)]
        # create embeddings
        res = openai.Embedding.create(input=list(lines_batch["content"]), engine=MODEL)
        embeds = [record['embedding'] for record in res['data']]
        # prep metadata and upsert batch
        meta = lines_batch.to_dict('records')
        to_upsert = zip(ids_batch, embeds, meta)
        # upsert to Pinecone
        index.upsert(vectors=list(to_upsert))
    time.sleep(60*60*5)







