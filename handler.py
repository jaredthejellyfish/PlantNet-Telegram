import json
import telegram
import os
import logging
import requests

from googleapiclient.discovery import build


def image_search(query):
    GOODLE_DEVKEY = os.environ.get("GOODLE_DEVKEY")
    GOOGLE_CX = os.environ.get("GOOGLE_CX")
    service = build("customsearch", "v1", developerKey=GOODLE_DEVKEY)

    res = (service.cse().list(
        q=query,
        cx=GOOGLE_CX,
        searchType="image",
        rights=
        "cc_publicdomain cc_attribute cc_sharealike cc_noncommercial cc_nonderived",
    ).execute())

    urls = [item["link"] for item in res["items"]]
    return urls[0]


# Logging is cool!
logger = logging.getLogger()
if logger.handlers:
    for handler in logger.handlers:
        logger.removeHandler(handler)
logging.basicConfig(level=logging.INFO)

OK_RESPONSE = {
    "statusCode": 200,
    "headers": {
        "Content-Type": "application/json"
    },
    "body": json.dumps("ok"),
}
ERROR_RESPONSE = {
    "statusCode": 400,
    "body": json.dumps("Oops, something went wrong!")
}


def configure_telegram():
    """
    Configures the bot with a Telegram Token.

    Returns a bot instance.
    """

    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if not TELEGRAM_TOKEN:
        logger.error("The TELEGRAM_TOKEN must be set")
        raise NotImplementedError

    return telegram.Bot(TELEGRAM_TOKEN)


def get_plant(url):

    img = requests.get(url).content
    PLANTNET_KEY = os.environ.get("PLANTNET_KEY")  # Set you API_KEY here
    api_endpoint = f"https://my-api.plantnet.org/v2/identify/all?api-key={PLANTNET_KEY}"

    data = {"organs": ["leaf"]}

    files = [("images", img)]

    req = requests.Request("POST", url=api_endpoint, files=files, data=data)
    prepared = req.prepare()
    s = requests.Session()
    response = s.send(prepared)

    results = json.loads(response.text)["results"][0]

    commonNames = results["species"]["commonNames"]
    family = results["species"]["family"]["scientificNameWithoutAuthor"]
    scientificName = results["species"]["scientificNameWithoutAuthor"]
    confidence = round((float(results["score"]) * 100), 1)
    commonNamesString = ""

    if len(commonNames) > 1:
        for name in commonNames:
            commonNamesString += f"  • {name}\n"
        if confidence < 12:
            out = f"This is <b>{scientificName}</b>, of the <b>{family}</b> family. \n\n<b>This plant is also known as:</b> \n{commonNamesString}"
        else:
            out = f"I'm {confidence}% sure this is <b>{scientificName}</b>, of the <b>{family}</b> family. \n\n<b>This plant is also known as:</b> \n{commonNamesString}"

    elif len(commonNames) == 1:
        commonNamesString = f"  • {commonNames[0]}"
        if confidence < 12:
            out = f"This is <b>{scientificName}</b>, of the <b>{family}</b> family. \n\n<b>This plant is also known as:</b> \n{commonNamesString}"
        else:
            out = f"I'm {confidence}% sure this is <b>{scientificName}</b>, of the <b>{family}</b> family. \n\n<b>This plant is also known as:</b> \n{commonNamesString}"

    else:

        if confidence < 12:
            out = f"This is <b>{scientificName}</b>, of the <b>{family}</b> family."
        else:
            out = f"I'm {confidence}% sure this is <b>{scientificName}</b>, of the <b>{family}</b> family."

    url = image_search(scientificName)

    return out, url


def get_file_url(update):

    TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

    file_id = update["message"]["photo"][-1]["file_id"]
    url_file_path = "https://api.telegram.org/bot{}/getFile?file_id={}".format(
        TELEGRAM_TOKEN, file_id)
    file_path = requests.get(url_file_path).json()["result"]["file_path"]
    file_url = "https://api.telegram.org/file/bot{}/{}".format(
        TELEGRAM_TOKEN, file_path)
    return file_url


def webhook(event, context):
    """
    Runs the Telegram webhook.
    """

    # TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

    bot = configure_telegram()
    logger.info("Event: {}".format(event))

    if event.get("httpMethod") == "POST" and event.get("body"):
        logger.info("Message received")
        update = telegram.Update.de_json(json.loads(event.get("body")), bot)
        chat_id = update.message.chat.id
        text = update.message.text

        if text == "/start":
            text = f"""Hello, <b>{update['message']['chat']['first_name']}</b>! \nI'm a bot designed to help you identify any plant you want. \nJust send me a photo and I will be more than glad to tell you what plant it is!"""
        else:
            try:
                file_url = get_file_url(update)
                text, url = get_plant(file_url)

                bot.send_photo(
                    chat_id=chat_id,
                    photo=url,
                    caption=text,
                    parse_mode=telegram.ParseMode.HTML,
                )

            except Exception as error:
                text = "I'm sorry but I could not Identify this plant :/"
                error_string = repr(error)
                bot.sendMessage(chat_id=chat_id, text=text)
                bot.sendMessage(chat_id=chat_id,
                                text=f"The reported error is: {error_string}")
                return OK_RESPONSE

        logger.info("Message sent")

        return OK_RESPONSE

    return ERROR_RESPONSE


def set_webhook(event, context):
    """
    Sets the Telegram bot webhook.
    """

    logger.info("Event: {}".format(event))
    bot = configure_telegram()
    url = "https://{}/{}/".format(
        event.get("headers").get("Host"),
        event.get("requestContext").get("stage"),
    )
    webhook = bot.set_webhook(url)

    if webhook:
        return OK_RESPONSE

    return ERROR_RESPONSE
