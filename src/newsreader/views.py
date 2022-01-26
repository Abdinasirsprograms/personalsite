import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import ensure_csrf_cookie
from django.shortcuts import render
from .models import *
import logging
logging.basicConfig(level=logging.DEBUG) # Here

@ensure_csrf_cookie
def display_html(request):
        return render(request, 'newsreader/base.html')

def pull_articles(request, language):
        # data = Article_links.objects.filter(site__language=language).order_by('-date_posted')[:50]
        context = {}
        sites = Article_site.objects.filter(language=language)
        for site in sites:
                content = []
                data = Article_links.objects.filter(site__id=site.id).order_by('-date_posted')[:15]
                for count, article in enumerate(data):
                        temp = []
                        temp = [{       'id' : article.id,
                                        'site': article.site.domain,
                                        'external_link': article.article_link,
                                        'date_posted':article.date_posted,
                                        'description': article.description,
                                        'title': article.title
                        }]
                        content.append(temp)
                context[site.domain] = content
        return JsonResponse({'data': context})

@require_http_methods(['POST'])
def return_proxy(request):
        try:
                received_data = json.loads(request.body)
                if not received_data: raise ValueError
                return JsonResponse({'status': 'loading'})

        except ValueError:
                logging.error(f'\n!!! \nPOST data is empty: {request.POST} I think? : {received_data}\n!!!')
                return JsonResponse({'receivedValue': received_data}, status="400")
        