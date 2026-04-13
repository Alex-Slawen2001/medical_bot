import random
from aiogram import F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from services import get_facts


class FactState(StatesGroup):
    choosing = State()


# ---------- клавиатуры ----------
def source_kb():
    b = InlineKeyboardBuilder()
    b.button(text="📰 MedlinePlus", callback_data="med")
    b.button(text="💊 FDA", callback_data="fda")
    b.adjust(1)
    return b.as_markup()


def more_kb():
    b = InlineKeyboardBuilder()
    b.button(text="🔄 Ещё факт", callback_data="more")
    return b.as_markup()


# ---------- регистрация ----------
def register_handlers(dp):

    @dp.message(Command("start"))
    async def start(message: Message, state: FSMContext):
        await state.set_state(FactState.choosing)
        await message.answer("Выбери источник:", reply_markup=source_kb())


    @dp.callback_query(F.data.in_(["med", "fda"]))
    async def choose_source(callback: CallbackQuery, state: FSMContext):
        source = callback.data
        await state.update_data(source=source, history=[])

        await send_fact(callback.message, state)
        await callback.answer()


    @dp.callback_query(F.data == "more")
    async def more(callback: CallbackQuery, state: FSMContext):
        await send_fact(callback.message, state)
        await callback.answer()


# ---------- логика ----------
async def send_fact(message: Message, state: FSMContext):
    data = await state.get_data()
    source = data.get("source")

    if not source:
        await message.answer("Сначала выбери источник через /start")
        return

    facts = get_facts(source)

    if not facts:
        await message.answer("😕 Нет данных")
        return

    history = data.get("history", [])

    # убираем повторения
    available = [f for f in facts if f not in history]
    if not available:
        history = []
        available = facts

    fact = random.choice(available)
    history.append(fact)

    await state.update_data(history=history)

    await message.answer(
        fact,
        reply_markup=more_kb(),
        parse_mode="HTML"
    )