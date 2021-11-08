from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
class Article_site(models.Model):
    link_to_site = models.URLField()
    domain = models.CharField(max_length=80)
    language = models.CharField(
        max_length=2,
        choices=[
            ('EN', 'English'), ('SO', 'Somali')
        ],
        default='EN',
    )

    website_type = models.CharField(
        max_length=4,
        choices=[
            ('XML', 'XML'), ('HTML', 'HTML')
        ],
        default='HTML',
    )
    class Meta:
            verbose_name = 'Site to pull article links from'
            verbose_name_plural = 'Sites to pull article links from'
    
    def __str__(self):
        return f"{self.domain} - {self.language}"
class Article_links(models.Model):
    article_link = models.URLField(max_length=255, unique=True) 
    site = models.ForeignKey(Article_site, on_delete=models.CASCADE, verbose_name="article's main site")
    date_posted = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    author = models.CharField(max_length=100, blank=True)
    title = models.CharField(max_length=255, blank=True)
    scrapped = models.BooleanField(default=False)
    class Meta:
            verbose_name = 'A Link to an article'
            verbose_name_plural = 'Links to articles'

    def __str__(self):
        return f"{self.title} * from {self.site}"
class Article_content(models.Model):
    title = models.CharField(max_length=255)
    date_posted = models.DateField(null=True, blank=True)
    author = models.CharField(max_length=100, blank=True)
    article_content = models.TextField()
    link_to_content = models.OneToOneField(Article_links, on_delete=models.CASCADE, verbose_name="article's link", unique=True)
    def save(self, *args, **kwargs):
        site_id = self.link_to_content.site.id
        site_articles = Article_links.objects.filter(article_content__article_content__isnull=False).filter(site__id=site_id)
        article_count = site_articles.count()
        if article_count >= 20:
            site_articles_by_date = site_articles.order_by('-date_posted')
            oldest_article = site_articles_by_date[article_count - 1].date_posted
            date_diff = oldest_article - self.date_posted
            if (date_diff.days <= -1):
                site_articles_by_date[article_count - 1].article_content.delete()
                super().save(*args, **kwargs)
            else:
                return
        super().save(*args, **kwargs) 
    class Meta:
            verbose_name = 'Article Data'
            verbose_name_plural = 'Article Data'

    def __str__(self):
        return f"{self.title} * from {self.link_to_content.site}"

