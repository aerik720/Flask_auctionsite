from flask import Blueprint

# Skapar en Blueprint för admin
admin_bp = Blueprint(
    'admin_bp',
    __name__,
    template_folder='templates', 
    static_folder='static'
)

from . import admin_routes