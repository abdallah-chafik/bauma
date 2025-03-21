
from django.contrib.auth.backends import BaseBackend
from .utils import JSONUserStorage
from werkzeug.security import check_password_hash

class JSONFileBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        user_storage = JSONUserStorage()
        user = user_storage.get_user_by_email(email)

        if user and check_password_hash(user['password'], password):
            return user
        return None

    def get_user(self, user_id):
        user_storage = JSONUserStorage()
        users = user_storage.load_users()
        for user in users:
            if user['id'] == user_id:
                return user
        return None