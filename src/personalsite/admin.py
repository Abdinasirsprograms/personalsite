from django.apps import apps
from django.utils.text import capfirst
from django.utils.translation import gettext as _, gettext_lazy
from django.template.response import TemplateResponse
from django.http import Http404
from django.contrib import admin
from django.contrib.admin import AdminSite


class CustomOrderingSite(AdminSite):
    site_header = 'Abdinasir\'s Amazing Website'
    site_title = "Abdinasir\'s Website Admin Portal"
    index_title = "Abdinasir\'s Amazing Website Portal"
    def get_app_list(self, request):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site.
        """
        ordering = {
                "Sites to pull article links from": 1,
                "Links to articles": 2,
                "Article Data": 3,
            }

        app_dict = self._build_app_dict(request)

        # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())

        # Specific ordering is enforced for NewsReader
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']] if x['name'] in ordering.keys() else x['name'])
        
        return app_list


    def app_index(self, request, app_label, extra_context=None):
        app_dict = self._build_app_dict(request, app_label)
        if not app_dict:
            raise Http404('The requested admin page does not exist.')
        ordering = {
                "Sites to pull article links from": 1,
                "Links to articles": 2,
                "Article Data": 3,
            }
        # Sort the models alphabetically within each app.
        app_dict['models'].sort(key=lambda x: ordering[x['name']] if x['name'] in ordering.keys() else x['name'])
        app_name = apps.get_app_config(app_label).verbose_name
        context = {
            **self.each_context(request),
            'title': _('%(app)s administration') % {'app': app_name},
            'app_list': [app_dict],
            'app_label': app_label,
            **(extra_context or {}),
        }

        request.current_app = self.name

        return TemplateResponse(request, self.app_index_template or [
            'admin/%s/app_index.html' % app_label,
            'admin/app_index.html'
        ], context)
