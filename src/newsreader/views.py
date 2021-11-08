from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import *

def display_html(request):
        return render(request, 'newsreader/index.html')

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

def display_article(request):
        return render(request, 'weather/base.html')