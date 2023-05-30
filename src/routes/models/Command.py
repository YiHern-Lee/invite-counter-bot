from telegram import Update
from telegram.ext import ContextTypes
from typing import Callable

class Command:
    def __init__(self, commandKeyWord: str, commandFunc: Callable[[Update, ContextTypes.DEFAULT_TYPE], None]):
        self._commandKeyWord = commandKeyWord
        self._commandFunc = commandFunc
    
    def getCommand(self) -> tuple[str, Callable[[Update, ContextTypes.DEFAULT_TYPE], None]]:
        return self._commandKeyWord, self._commandFunc
    
