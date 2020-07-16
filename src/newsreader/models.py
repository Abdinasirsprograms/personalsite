from django.db import models

class Article_site(models.Model):
    link_to_site = models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
class Article_link(models.Model):
    article_link = models.CharField(max_length=30, unique=True) 
    site = models.ForeignKey(Article_site, on_delete=models.CASCADE, verbose_name="article's main site")
    date_posted = models.DateField()
    description = models.CharField(max_length=30)
    author = models.CharField(max_length=30)
    title = models.CharField(max_length=30)
class Article_content(models.Model):
    title = models.CharField(max_length=30)
    date_posted = models.DateField()
    author = models.CharField(max_length=30)
    article_content = models.CharField(max_length=30)
    link_to_content = models.OneToOneField(Article_link, on_delete=models.CASCADE, verbose_name="article's link")