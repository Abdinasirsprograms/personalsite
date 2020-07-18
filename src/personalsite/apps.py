from django.contrib.admin.apps import AdminConfig
from .admin import CustomOrderingSite
class MyAdminConfig(AdminConfig):
    default_site = 'personalsite.admin.CustomOrderingSite'