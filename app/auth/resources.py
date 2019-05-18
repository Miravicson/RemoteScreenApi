from flask_restful import Resource, reqparse
from .models import UserModel, RevokedTokenModel
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_required,
    jwt_refresh_token_required,
    get_jwt_identity,
    get_raw_jwt
)

parser = reqparse.RequestParser()

arguments = [('first_name', False), ('last_name', False),
             ('username', True), ('password', True)]


def configure_parser(parser, arguments):
    for argument in arguments:
        message = 'This field is optional'
        if argument[1]:
            message = 'This field is required'
        parser.add_argument(argument[0], help=message, required=argument[1])
    return parser


parser_reg = configure_parser(parser, arguments)
parser_login = configure_parser(parser, arguments[0:2])


class UserRegistration(Resource):
    def post(self):
        data = parser_reg.parse_args(strict=True)

        if UserModel.find_by_username(data['username']):
            return {"message": f"The username {data['username']} already exists"}

        data['password'] = UserModel.hash_password(data['password'])

        new_user = UserModel(**data)

        try:
            new_user.save_to_db()
            access_token = create_access_token(identity=new_user.username)
            refresh_token = create_refresh_token(identity=new_user.username)
            return {
                "message": f"The user {new_user.username} has been created",
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        except Exception as e:
            return {"message": "Something went wrong"}, 500


class UserLogin(Resource):
    def post(self):
        data = parser_login.parse_args(strict=True)
        current_user = UserModel.find_by_username(data['username'])
        if not current_user:
            return {
                'message': "Wrong username or password"
            }, 401
        elif UserModel.verify_password(data['password'], current_user.password):
            access_token = create_access_token(identity=current_user.username)
            refresh_token = create_refresh_token(
                identity=current_user.username)
            return {
                'message': f"Logged in as user {current_user.username}",
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        else:
            return {
                'message': "Wrong username or password"
            }, 401


class UserLogoutAcess(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {"message": "Access token has been revoked"}
        except:
            return {"message": "Something went wrong"}, 500


class UserLogoutRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_jwt_identity()['jti']
        try:
            revoked_token = RevokedTokenModel(jti=jti)
            revoked_token.add()
            return {"message": "Refresh token has been revoked"}
        except:
            return {"message": "Something went wrong"}, 500


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        access_token = create_access_token(identity=current_user)
        return {"access_token": access_token}


class AllUsers(Resource):
    def get(self):
        return UserModel.return_all()

    # def delete(self):
    #     return UserModel.delete_all()
