import logging
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from datetime import datetime
from model import session
from config import TELEGRAM_API
from model import DialogStates, Events
import asyncio

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TELEGRAM_API)
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer("Приветствую тебя в моем HandBook!\n /add - добавить событие \n /view - просмотреть события")
    while True:
        await asyncio.sleep(1)
        now = datetime.now()
        current_time = now.strftime("%y-%m-%d %H:%M")
        events = session.query(Events).all()
        for event in events:
            current_time_db = event.event_time.strftime("%y-%m-%d %H:%M")
            if current_time_db == current_time:
                await message.answer(f'Напоминание о событие <strong><u>{event.event_name}</u></strong>!', parse_mode=ParseMode.HTML)
                delete_event = session.query(Events).filter(Events.event_name == f'{event.event_name}').one()
                session.delete(delete_event)
                session.commit()


@dp.message(Command("add"))
async def add_event(message: types.Message, state: FSMContext):
    await message.answer('Введите название события')
    await state.set_state(DialogStates.name_event)


@dp.message(Command('view'))
async def view(message: types.Message):
    string = 'id | Название события | Время события \n'
    events = session.query(Events).all()
    for event in events:
        string += f'{event.id} | {event.event_name} | {event.event_time}\n'
    await message.answer(string)


@dp.message(Command('edit'))
async def edit(message: types.Message, state: FSMContext):
    await message.answer('Введите id события')
    await state.set_state(DialogStates.edit_event)


@dp.message(DialogStates.edit_event)
async def take_id(message: types.Message, state: FSMContext):
    event_time = message.text


@dp.message(DialogStates.name_event)
async def answer_first(message: types.Message, state: FSMContext):
    answer = message.text
    await state.update_data(event_name=answer)
    await message.answer("Введите время события")
    await state.set_state(DialogStates.time_event)


@dp.message(DialogStates.time_event)
async def answer_second(message: types.Message, state: FSMContext):
    data = await state.get_data()
    answer1 = data['event_name']
    answer2 = message.text
    await state.clear()
    event = Events(username="onedeadream", event_name=f'{answer1}', event_time=f'{answer2}')
    session.add(event)
    session.commit()
    await message.answer('Событие успешно добавлено!')


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
