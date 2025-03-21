from django.apps import AppConfig

class HomepageConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'homepage'
    verbose_name = 'Homepage'

    def ready(self):
        """
        Cette méthode est appelée lorsque l'application est prête.
        Vous pouvez y mettre du code d'initialisation si nécessaire.
        """
        # Importez vos signaux ici si vous en avez
        # from . import signals

        # Assurez-vous que le dossier data existe
        import os
        data_dir = os.path.join(os.path.dirname(__file__), 'data')
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)