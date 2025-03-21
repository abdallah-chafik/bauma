from django.views.generic import TemplateView, CreateView
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from .utils import JSONUserStorage
from werkzeug.security import generate_password_hash, check_password_hash
from django.views import View

class HomeView(TemplateView):
    template_name = 'homepage/home.html'

class CustomLoginView(View):
    template_name = 'homepage/auth/login.html'
    user_storage = JSONUserStorage()

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('homepage:profile')
        return render(request, self.template_name)

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            stored_user = self.user_storage.get_user_by_email(email)

            if stored_user and check_password_hash(stored_user['password'], password):
                request.session['user_id'] = stored_user['id']
                request.session['user_email'] = stored_user['email']
                request.session['user_name'] = f"{stored_user['first_name']} {stored_user['last_name']}"

                return redirect('homepage:profile')
            else:
                return render(request, self.template_name, {
                    'error': 'Email ou mot de passe incorrect'
                })

        except Exception as e:
            print(f"Erreur de connexion : {str(e)}")
            return render(request, self.template_name, {
                'error': 'Une erreur est survenue lors de la connexion'
            })

class RegisterView(View):
    template_name = 'homepage/auth/register.html'
    user_storage = JSONUserStorage()

    def get(self, request):
        return render(request, self.template_name)

    def post(self, request):
        data = request.POST
        try:
            if not all([data.get('first_name'), data.get('last_name'),
                       data.get('email'), data.get('password')]):
                raise ValueError("Tous les champs sont obligatoires")

            new_user = {
                'first_name': data['first_name'],
                'last_name': data['last_name'],
                'email': data['email'],
                'password': generate_password_hash(data['password']),
                'id': len(self.user_storage.load_users()) + 1
            }

            self.user_storage.add_user(new_user)
            return redirect('homepage:login')

        except ValueError as e:
            return render(request, self.template_name, {'error': str(e)})
        except Exception as e:
            return render(request, self.template_name,
                        {'error': "Une erreur est survenue lors de l'inscription"})

class ProfileView(View):
    template_name = 'homepage/auth/profile.html'
    user_storage = JSONUserStorage()

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('homepage:login')
        
        # Récupérer les informations à jour de l'utilisateur depuis le JSON
        user_id = request.session.get('user_id')
        users = self.user_storage.load_users()
        user_data = next((u for u in users if u['id'] == user_id), None)

        if not user_data:
            # Si l'utilisateur n'est pas trouvé, déconnexion
            logout(request)
            return redirect('homepage:login')

        context = {
            'user': {
                'id': user_data['id'],
                'email': user_data['email'],
                'first_name': user_data['first_name'],
                'last_name': user_data['last_name'],
                'full_name': f"{user_data['first_name']} {user_data['last_name']}",
            },
            'projects': [],  # Vous pouvez ajouter des projets ici si nécessaire
            'recent_activity': []  # Vous pouvez ajouter l'activité récente ici
        }
        
        return render(request, self.template_name, context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect('homepage:login')

        action = request.POST.get('action')
        
        if action == 'update_profile':
            try:
                user_id = request.session.get('user_id')
                users = self.user_storage.load_users()
                user_index = next((index for (index, u) in enumerate(users) 
                                 if u['id'] == user_id), None)

                if user_index is not None:
                    # Mise à jour des informations de l'utilisateur
                    users[user_index].update({
                        'first_name': request.POST.get('first_name', users[user_index]['first_name']),
                        'last_name': request.POST.get('last_name', users[user_index]['last_name']),
                        'email': request.POST.get('email', users[user_index]['email'])
                    })

                    # Si un nouveau mot de passe est fourni
                    new_password = request.POST.get('new_password')
                    if new_password:
                        users[user_index]['password'] = generate_password_hash(new_password)

                    # Sauvegarder les modifications
                    self.user_storage.save_users(users)
                    
                    # Mettre à jour la session
                    request.session['user_email'] = users[user_index]['email']
                    request.session['user_name'] = f"{users[user_index]['first_name']} {users[user_index]['last_name']}"

                    return render(request, self.template_name, {
                        'success': 'Profil mis à jour avec succès',
                        'user': users[user_index]
                    })

            except Exception as e:
                return render(request, self.template_name, {
                    'error': 'Erreur lors de la mise à jour du profil',
                    'user': request.user
                })

        return redirect('homepage:profile')

def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('homepage:login')

# Remplacer la vue fonction par la vue classe
profile_view = ProfileView.as_view()