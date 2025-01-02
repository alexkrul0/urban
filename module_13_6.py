from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

api = "-"
bot = Bot(token=api)
dp = Dispatcher(bot, storage=MemoryStorage())

kb = ReplyKeyboardMarkup(resize_keyboard=True)
button_calc = KeyboardButton(text='Рассчитать')
button_info = KeyboardButton(text='Информация')
# kb.row(button_info, button_calc)
kb.add(button_info)
kb.add(button_calc)

kb_in = InlineKeyboardMarkup()
button_calor = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
button_formula = InlineKeyboardButton(text='Формула расчета', callback_data='formula')
# kb_in.add(button_calor)
# kb_in.add(button_formula)
kb_in.row(button_calor, button_formula)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()


@dp.callback_query_handler(text='calories')
async def set_age(call):
    await call.message.answer('Введите свой возраст.')
    await UserState.age.set()


@dp.callback_query_handler(text='formula')
async def get_formula(call):
    await call.message.answer('10 * вес(кг) + 6,25 * рост(см) - 5 * возраст(лет) - 161')


@dp.message_handler(text='Рассчитать')
async def main_menu(message):
    await message.answer('Выберите опцию:', reply_markup=kb_in)


@dp.message_handler(state=UserState.age)
async def set_growth(message, state):
    await state.update_data(first=message.text)
    await message.answer('Введите свой рост.')
    await UserState.growth.set()


@dp.message_handler(state=UserState.growth)
async def set_weight(message, state):
    await state.update_data(second=message.text)
    await message.answer('Введите свой вес.')
    await UserState.weight.set()


@dp.message_handler(state=UserState.weight)
async def send_calories(message, state):
    await state.update_data(third=message.text)
    data = await state.get_data()
    calors = 10 * int(data['third']) + 6.25 * int(data['second']) - 5 * int(data['first'])
    await message.answer(f'Ваша норма калорий {calors}')
    await state.finish()


@dp.message_handler(commands=['start'])
async def start(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью.', reply_markup=kb)


@dp.message_handler()
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
