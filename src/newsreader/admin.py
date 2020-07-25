from django.contrib import admin
from django import forms
from django.utils.html import format_html

from .models import *
class Display_id_Sites(admin.ModelAdmin):
    list_display = ['id', 'link_to_site', 'domain', 'language', 'website_type']
    ordering = ('id',)
    list_editable = ['language']
class Display_id_Links(admin.ModelAdmin):
    list_display = ['id', 'site', 'date_posted', 'author', 'title', 'scrapped', 'get_article_content']
    def get_article_content(self, obj):
        article_id = Article_content.objects.get(link_to_content__exact=obj.id).id
        return format_html('<a href="/admin/newsreader/article_content/{}" target="_blank">{}</a>', 
        article_id, article_id)
    get_article_content.short_description = 'article content id'
    ordering = ('id',)
    list_editable = ['scrapped']

class Display_id_Articles(admin.ModelAdmin):
    list_display = ['id', 'get_articles_site', 'title', 'date_posted', 'author', 'get_actual_link', 'get_language']
    list_editable = ['author']
    def get_actual_link(self, obj):
        return format_html('<a href="{}" target="_blank">Link to Article</a>', 
        obj.link_to_content.article_link, obj.link_to_content.article_link)
    def get_language(self, obj):
        return obj.link_to_content.site.language
    def get_articles_site(self, obj):
        return obj.link_to_content.site
    def get_empty_article_links(self, obj):
        empty = Article_links.objects.filter(article_content__link_to_content__isnull=True)
        for empty_article in empty:
            return empty.id 
    get_actual_link.short_description = 'Link to article'
    get_articles_site.short_description = 'Article\'s main site'
    get_language.short_description = 'Language'
    get_language.admin_order_field = 'link_to_content__site__language'
    ordering = ('id',)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "link_to_content":
            kwargs["queryset"] = Article_links.objects.filter(article_content__link_to_content__isnull=True)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

admin.site.register(Article_site, Display_id_Sites)
admin.site.register(Article_links, Display_id_Links)
admin.site.register(Article_content, Display_id_Articles)
