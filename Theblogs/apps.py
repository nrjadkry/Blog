from django.apps import AppConfig


class TheblogsConfig(AppConfig):
    name = 'Theblogs'

    def ready(self):
    	import Theblogs.signals