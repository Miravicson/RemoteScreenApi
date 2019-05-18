from .resources import UserRegistration, UserLogin, UserLogoutAcess, UserLogoutRefresh, AllUsers, TokenRefresh
from flask_restful import Api
from . import bp

api = Api()
api.init_app(bp)
api.add_resource(UserRegistration, '/auth/register')
api.add_resource(UserLogin, '/auth/login')
api.add_resource(UserLogoutAcess, '/auth/logout/access')
api.add_resource(UserLogoutRefresh, '/auth/logout/refresh')
api.add_resource(TokenRefresh, '/auth/token/refresh')
api.add_resource(AllUsers, '/auth/users')

