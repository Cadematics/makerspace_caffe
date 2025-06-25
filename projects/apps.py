from django.apps import AppConfig


class ProjectsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'


class UsersConfig(AppConfig):  # Or your app name
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'projects'  # Make sure this matches your folder name

    def ready(self):
        import projects.signals  # This line registers the signals

        