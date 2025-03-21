# homepage/utils.py
import json
import os
from pathlib import Path

class JSONUserStorage:
    def __init__(self):
        self.file_path = Path(__file__).parent.parent / 'data' / 'users.json'
        self.ensure_file_exists()

    def ensure_file_exists(self):
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        if not os.path.exists(self.file_path):
            # Initialiser avec un tableau vide
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=4, ensure_ascii=False)

    def load_users(self):
        try:
            with open(self.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return json.loads(content) if content else []
        except json.JSONDecodeError:
            return []

    def save_users(self, users):
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4, ensure_ascii=False)

    def add_user(self, user_data):
        users = self.load_users()
        # Vérifier si l'email existe déjà
        if any(user['email'] == user_data['email'] for user in users):
            raise ValueError("Cette adresse email est déjà utilisée.")
        users.append(user_data)
        self.save_users(users)

    def get_user_by_email(self, email):
        users = self.load_users()
        for user in users:
            if user['email'] == email:
                return user
        return None