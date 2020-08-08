from django.http import JsonResponse
from django.core.paginator import Paginator
from django.shortcuts import render
from .models import *

def display_html(request):
        return render(request, 'newsreader/index.html')

def pull_articles(request, language):
        data = Article_links.objects.filter(site__language=language)
        context = []
        data = Paginator(data,50)
        data = data.page(1).object_list
        for article in data:
                temp = {}
                temp['site'] = article.site.domain
                temp['external_link'] = article.article_link
                temp['date_posted'] = article.date_posted
                temp['description'] = article.description
                temp['title'] = article.title
                context.append({'id': article.id, 'content':temp})
                        
        return JsonResponse({'data': context})

def display_article(request):
        return render(request, 'weather/base.html')