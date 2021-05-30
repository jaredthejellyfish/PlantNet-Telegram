# Serverless Telegram Bot
This example demonstrates how to setup an echo Telegram Bot using the Serverless Framework ⚡🤖

## Usage

### What do I need?
- A AWS key configured locally, see [here](https://serverless.com/framework/docs/providers/aws/guide/credentials/).
- Python 3.7.
- NodeJS. I tested with v8.9.0.
- A Telegram account.

### Installing
```
# Install the Serverless Framework
$ npm install serverless -g

# Install the necessary plugins
$ npm install

# Create and active a Python 3.7 venv
$ python3.7 -m venv venv && souce venv/bin/activate

# Get a bot from Telegram, sending this message to @BotFather
$ /newbot

# Put the token received into a file called serverless.env.yml, like this
$ cat serverless.env.yml
TELEGRAM_TOKEN: <your_token>

# Deploy it!
$ serverless deploy

# With the URL returned in the output, configure the Webhook
$ curl -X POST https://<your_url>.amazonaws.com/dev/set_webhook
```

Now, just start a conversation with the bot :)
# PlantNet-Telegram