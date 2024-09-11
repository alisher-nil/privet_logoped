from typing import Dict

from pydantic import BaseModel, Field
from schemas.menu import MenuItem


class ChatConfig(BaseModel):
    main_menu_items: Dict[int, MenuItem] = Field({})


chat_config = ChatConfig()
