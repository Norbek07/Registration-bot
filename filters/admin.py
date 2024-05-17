from aiogram.filters import BaseFilter
from aiogram.types import Message

class IsAdminFilter(BaseFilter):

    def __init__(self,telegram_id:list):
        self.telegram_ids = telegram_id
    
    async def __call__(self,message:Message):

        return message.from_user.id in self.telegram_ids