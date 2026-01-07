from flask import Blueprint

# Skapar en Blueprint för autentisering
auth_bp = Blueprint(
    'auth_bp',
    __name__,
    url_prefix='/auth',
    template_folder="templates")

from dbrepository.user_repo import user_repo
from . import auth_routes