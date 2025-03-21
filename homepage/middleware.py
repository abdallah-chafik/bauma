# homepage/middleware.py
from django.shortcuts import redirect
from django.urls import reverse
from .utils import JSONUserStorage

class JSONAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.user_storage = JSONUserStorage()

    def __call__(self, request):
        # Vérifier si l'utilisateur est connecté via session
        user_id = request.session.get('user_id')

        if user_id:
            # Récupérer les informations de l'utilisateur
            users = self.user_storage.load_users()
            user = next((u for u in users if u['id'] == user_id), None)

            if user:
                request.user = type('User', (), {
                    'is_authenticated': True,
                    'id': user['id'],
                    'email': user['email'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'get_full_name': lambda: f"{user['first_name']} {user['last_name']}"
                })
            else:
                request.user = type('AnonymousUser', (), {'is_authenticated': False})
        else:
            request.user = type('AnonymousUser', (), {'is_authenticated': False})

        response = self.get_response(request)
        return response