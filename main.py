from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, User
import random

BOT_TOKEN = ''

ATTEMPTS = 5

user_data = {
    'in_game':False,
    'atempts':None,
    'number':None,
    'amount_games':0,
    'wins':0
}

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

def generate_number() -> int:
     return random.randint(1, 100)

@dp.message(CommandStart())
async def process_start(message:Message):
    user:User|None = message.from_user
    name:str = user.first_name # type: ignore
    await message.answer(f'Hello {name}!!!\n I am bot with who you can play game "Guess The Number"\n press /help to learn rules and bot commands"')

@dp.message(Command(commands='help'))
async def process_help(message:Message):
     await message.answer(f'I will generate number between 0 and 100 and you need to guess it within {ATTEMPTS} attempts. Write play to start\n /cancel to stop the game\n /stat to see your statistic')

@dp.message(Command(commands='stat'))
async def process_stat(message:Message):
     await message.answer(f'Amount of games you play:{user_data['amount_games']}\nAmount of games you win {user_data['wins']}')

@dp.message(F.text.lower().contains("play"))
async def process_play(message:Message):
    if not user_data['in_game']:
          user_data['in_game'] = True
          user_data['atempts'] = ATTEMPTS
          user_data['number'] = generate_number()

          await message.answer(f'Game started you have {ATTEMPTS} attemps')
    else:
         await message.answer('You are already playing')

@dp.message(Command(commands='cancel'))
async def process_cancel(message:Message):
    if user_data['in_game']:
         user_data['in_game'] = False
         user_data['atempts'] = None
         user_data['amount_games']+=1
         await message.answer('You stoped the game')
    else:
         await message.answer('you dont play now\nwrite play to start')

@dp.message(F.text.isdigit())
async def procces_number(message:Message):
     number:int = int(message.text) # type: ignore
     if user_data['in_game']:
          if number == user_data['number']:
               user_data['in_game'] = False
               user_data['atempts'] = None
               user_data['wins'] +=1
               user_data['amount_games'] += 1
               user_data['number'] = None
               await message.answer("Congratulations you win")
          elif number < user_data['number']:
               user_data['atempts'] -= 1
               await message.answer('no, the number is bigger')
          elif number > user_data['number']:
               user_data['atempts'] -= 1
               await message.answer('no, the number is smaller')

          if user_data['atempts'] == 0:
               user_data['in_game'] = False
               user_data['atempts'] = None
               user_data['amount_games'] += 1
               user_data['number'] = None
               await message.answer('you lost')

     else:
          await message.answer('start game before write numbers')

@dp.message()
async def process_other(message:Message):
     await message.answer('dont write other things. use only commands and numbers when you play')


if __name__ == '__main__':
     dp.run_polling(bot)