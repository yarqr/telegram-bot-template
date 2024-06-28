from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.text import Const

from src.presentation.telegram.states import StartSG

start = Dialog(Window(Const("Hello!"), state=StartSG.main))
