from flask import Blueprint

bp = Blueprint('auth', __name__)

from . import views
from .models import RevokedTokenModel