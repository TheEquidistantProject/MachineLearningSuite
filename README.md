# The Equidistant Project - Machine Learning Suite

![Equidistant Project Logo](insert_logo_url_here)

Welcome to the Machine Learning Suite repository of The Equidistant Project. This repository houses the code and resources for our mission to combat misinformation and bias in the news sphere through data scraping, text embeddings, and unbiased article generation.

## Table of Contents
- [Project Overview](#project-overview)
- [Workflow](#workflow)
- [Cosine Similarity](#cosine-similarity)
- [Stable Matching Problem](#stable-matching-problem)
- [The Instruct Model](#the-instruct-model)
- [Automated Scraping](#automated-scraping)
- [Dependencies](#dependencies)
- [Getting Started](#getting-started)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Project Overview

The Equidistant Project stands as a beacon against the tide of misinformation and bias prevalent in the news sphere. Our mission is to create a platform where users can access and interpret factual news. To achieve this goal, we have devised a multi-step process that involves scraping diverse news articles, extracting the factual essence, and crafting new, unbiased articles.

### Workflow

Our workflow can be summarized as follows:

1. **Data Scraping**: We scrape news websites, including sources such as Fox News and CNN, to collect a wide range of news articles.

2. **Text Embeddings**: Text embeddings are generated for each article using the GPT-3 Ada Model. This helps us represent the content in a numerical format for further analysis.

3. **Cosine Similarity**: We calculate cosine similarity between articles based on their body text. This allows us to pair articles with similar content.

### Cosine Similarity

In our workflow, we employ **cosine similarity** to measure the similarity between news articles based on their body text. Cosine similarity is a metric that quantifies the cosine of the angle between two non-zero vectors in a multi-dimensional space. In our case, each news article is represented as a vector in this space, and the cosine similarity score indicates how closely the articles align in content. This similarity metric helps us pair articles with similar content, facilitating further analysis and article generation.

### Stable Matching Problem

The process of pairing articles based on their content can be analogously related to the **Stable Matching Problem** in the field of mathematics and computer science. In the Stable Matching Problem, entities from two groups are paired in a way that there are no pairs of entities that both prefer each other over their current partners. Similarly, in our project, we aim to pair articles in a way that maximizes content alignment while minimizing the potential for misinformation.

4. **Prompt Generation**: We design specific prompts to align the GPT-3.5-turbo-instruct model to produce balanced and unbiased articles. These prompts play a crucial role in preventing misinformation.

### The Instruct Model

To ensure that our generated articles are as unbiased and accurate as possible, we have selected the **GPT-3.5-turbo-instruct model**. This model has been fine-tuned and further refined using **Reinforcement Learning with human feedback**. This rigorous fine-tuning process is crucial in aligning the model's behavior with our goal of preventing misinformation.

The fine-tuning with human feedback involves iteratively training the model, receiving human evaluators' feedback, and adjusting the model's parameters accordingly. This process helps the model generate more balanced, informative, and less biased content, making it a valuable tool in our mission to provide factual and unbiased news articles.

### Automated Scraping

To ensure that our news articles are up-to-date, we have implemented an **automated scraping process** that runs periodically. This process involves:

- Scheduling a script to run at predefined intervals using a task scheduler or cron job.
- The script initiates the data scraping process, collecting new articles from news websites.
- New articles are processed, and text embeddings are generated as part of our workflow.
- The newly scraped articles are then stored in our database (MongoDB Atlas) alongside their embeddings.
- Existing articles are also periodically updated to ensure their relevance.

This automation ensures that our platform always provides the latest and most relevant news articles to our users.

## Dependencies

Before you begin, ensure you have met the following requirements:

- Python 3.x
- Dependencies listed in `requirements.txt`

## Getting Started

To get started with the Equidistant Project Machine Learning Suite repository, follow these steps:

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/TheEquidistantProject/MachineLearningSuite.git
   ```

2. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Set up your Pinecone and MongoDB Atlas credentials as specified in the configuration files.

## Usage

`docker-compose up --build`


## License

This project is licensed under the [MIT License](LICENSE).

---

Thank you for joining us in our mission to combat misinformation and promote unbiased news. Together, we can create a more enlightened public discourse. If you have any questions or feedback, please don't hesitate to [contact us](mailto:contact@equidistantproject.com).