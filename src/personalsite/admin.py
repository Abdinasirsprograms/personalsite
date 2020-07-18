from django.contrib import admin
from django.contrib.admin import AdminSite


class CustomOrderingSite(AdminSite):

    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering = {
                "Sites to pull article links from": 1,
                "Links to articles": 2,
                "Article links to pull article data from": 3,
            }

        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Specific ordering is enforced for NewsReader
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']] if x['name'] in ordering.keys() else x['name'])
        
        return app_list
