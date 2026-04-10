from django.apps import AppConfig


class ShopnameConfig(AppConfig):
    name = 'shopname'

    def ready(self) -> None:
        import shopname.signals