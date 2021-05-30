# PlantNet-Telegram
A plant identification Telegram bot! ⚡🤖

## Usage

### What do I need?
- A AWS key configured locally, see [here](https://serverless.com/framework/docs/providers/aws/guide/credentials/)
- Python 3 (Tested with Python 3.9)
- NodeJS (Tested with v8.9.0)
- A Telegram account.

### Install Requirements
```
# Install the Serverless Framework
$ npm install serverless

# Install the necessary plugin
$ npm install serverless-python-requirements
```

### Enable Custom Search API & Get your API Key
- Visit [Google Developer Console](https://console.developers.google.com) and create a project.
- Go to [Google Custom Search API](https://console.cloud.google.com/marketplace/product/google/customsearch.googleapis.com?pli=1)and enable "Custom Search API" for your project.
- Visit [Developer Credentials](https://console.developers.google.com/apis/credentials) and generate API key credentials for your project.

### Get google CX key
- Go to [Google CSE](https://cse.google.com/all).
- Create your search engine.
- In the web form where you create/edit your custom search engine enable "Image search" option and for "Sites to search" option select "Search the entire web but emphasize included sites".
- You can find the CX id titled as "Search engine ID".
- Public URL also has the cx id in the Query param as ?cx=**

### Get PlantNet API Key
- Follow the steps listed here [PlantNet API how to](https://my.plantnet.org/usage).

### Create Telegram Bot
- Start a chat with the [BotFather](https://telegram.me/botfather)
- Create a new bot with the command ```/newbot```
- Specify a friendly name
- Specify a username
- Copy the access token