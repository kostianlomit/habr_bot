import logging

from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery


from loader import dp, bot
from test import get_tasks, url, task_name, pars_json


@dp.message_handler(Command("start"))
async def show_items(message: Message):
    await message.answer(text="please wait 2-3 minutes... pars values")
    get_tasks(url, task_name)

#
@dp.message_handler(Command("items"))
async def show_items(message: Message):
    await message.answer("Please waiting...")

    a = pars_json()
    for i in a:
        await message.answer(i)
