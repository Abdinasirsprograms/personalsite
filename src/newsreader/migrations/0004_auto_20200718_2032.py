# Generated by Django 3.0.8 on 2020-07-19 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('newsreader', '0003_auto_20200718_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article_content',
            name='author',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='article_content',
            name='date_posted',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article_links',
            name='author',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='article_links',
            name='date_posted',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='article_links',
            name='description',
            field=models.CharField(blank=True, max_length=120),
        ),
        migrations.AlterField(
            model_name='article_links',
            name='title',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='article_site',
            name='name',
            field=models.CharField(max_length=30),
        ),
    ]
