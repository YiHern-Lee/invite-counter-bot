from typing import Callable, TypeVar

from telegram import Update
from telegram.ext import ContextTypes
from telegram.ext.filters import BaseFilter
from telegram.ext._utils.types import CCT, HandlerCallback

RT = TypeVar("RT")

class MessageAction:
    def __init__(self, messageFilter: BaseFilter, messageFunc: HandlerCallback[Update, CCT, RT]):
        self._messageFilter = messageFilter
        self._messageFunc = messageFunc
    
    def getMessageAction(self) -> tuple[BaseFilter, HandlerCallback[Update, CCT, RT]]:
        return self._messageFilter, self._messageFunc
    
