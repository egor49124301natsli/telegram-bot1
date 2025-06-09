from .users import register_handlers as register_user_handlers
from .admin import register_handlers as register_admin_handlers
from .premium import register_handlers as register_premium_handlers

def register_handlers(dp):
    register_user_handlers(dp)
    register_admin_handlers(dp)
    register_premium_handlers(dp)
