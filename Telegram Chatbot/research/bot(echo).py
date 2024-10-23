# Checking where I will be able to connect with my telegram or not
# Click on bootfather verified in telegram app
# Create a new bot there and collect the token and save it in the env file

# For Reference:- https://docs.aiogram.dev/en/dev-3.x/


import logging
from aiogram import Bot, Dispatcher,  types , executor
from dotenv import load_dotenv
import os

# Load the APi key
load_dotenv()
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# print(TELEGRAM_BOT_TOKEN)

#configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN) # Bot will be initialized, If True, Dispatcher will be connected
dp = Dispatcher(bot) # Synchronization(What ever message I will Pass), It will go to telegram bot


# async:- It will keep on sensing for the update and then it will automatically pass with the help of (await)

# Start/Help :- In telegram text we give /start and/ help , then It will give the menu
# Specific command
@dp.message_handler(commands=['start', 'help'])
async def command_start_handler(message: types.Message):  
    """
    This handler receives messages with `/start` or  `/help `command
    """
    await message.reply("Hi\nI am Echo Bot!\nPowered by Priyanshu.")

# When ever we will type the message start or help it will give the await message
# It will not handle my normal message for that we will use llm


# Casual Command
@dp.message_handler()
async def echo(message: types.Message): # User message
    """
    This will retrun echo
    """
    await message.answer(message.text) # Same output


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)



