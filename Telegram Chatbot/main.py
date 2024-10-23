from dotenv import load_dotenv
import os
from aiogram import Bot, Dispatcher, executor, types
import openai
import sys

# Load the keys
load_dotenv()
openai.api_key = os.getenv("OpenAI_API_KEY")  
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


class Reference:
    '''
    A class to store previously response from the openai API
    '''
    # Store all the responses, For remembering anything
    def __init__(self) -> None:
        self.response = ""


# Initialize
reference = Reference()
model_name = "gpt-3.5-turbo-0125"



# Initialize bot and dispatcher(Authentication)
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dispatcher = Dispatcher(bot)


# Clear  saved Conversation
def clear_past():
    """A function to clear the previous conversation and context.
    """
    reference.response = ""

@dispatcher.message_handler(commands=['clear'])
async def clear(message: types.Message):
    """
    A handler to clear the previous conversation and context.
    """
    clear_past()
    await message.reply("I've cleared the past conversation and context.")



# Welcome Message
@dispatcher.message_handler(commands=['start'])
async def welcome(message: types.Message):
    """
    This handler receives messages with `/start` or  `/help `command
    """
    await message.reply("Hi\nI am Tele Bot!\Created by Priyanshu . How can i assist you?")


# Help Message
@dispatcher.message_handler(commands=['help'])
async def helper(message: types.Message):
    """
    A handler to display the help menu.
    """
    help_command = """
    Hi There, I'm Telegram bot created by Priyanshu ! Please follow these commands - 
    /start - to start the conversation
    /clear - to clear the past conversation and context.
    /help - to get this help menu.
    I hope this helps. :)
    """
    await message.reply(help_command)




# Normal Template
@dispatcher.message_handler()
async def chatgpt(message: types.Message):
    """
    A handler to process the user's input and generate a response using the chatGPT API.
    """
    print(f">>> USER: \n\t{message.text}")
    response = openai.ChatCompletion.create(
        model = model_name,
        messages = [
            {"role": "assistant", "content": reference.response}, # role assistant # Previous Response, if any
            {"role": "user", "content": message.text} #our query 
        ]
    )
    reference.response = response['choices'][0]['message']['content'] # Only printing the content
    print(f">>> chatGPT: \n\t{reference.response}")
    await bot.send_message(chat_id = message.chat.id, text = reference.response) # Printing in telegram


if __name__ == "__main__":
    executor.start_polling(dispatcher, skip_updates=False) 

# skip_updates(False):- If my app is offline and if i give a prompt , it will not run
#                         and when it will go online , it will automatically run theprompt in offline mode

# With help of telegram user name we can access it 
