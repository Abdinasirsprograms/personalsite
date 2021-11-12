# Generated by Django 3.0.8 on 2020-07-18 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article_site',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link_to_site', models.URLField()),
                ('name', models.CharField(max_length=30, null=True)),
                ('language', models.CharField(choices=[('EN', 'English'), ('SO', 'Somali')], default='EN', max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Article_links',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article_link', models.URLField(max_length=255, unique=True)),
                ('date_posted', models.DateField(null=True)),
                ('description', models.CharField(max_length=120, null=True)),
                ('author', models.CharField(max_length=100, null=True)),
                ('title', models.CharField(max_length=100, null=True)),
                ('site', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='newsreader.Article_site', verbose_name="article's main site")),
            ],
        ),
        migrations.CreateModel(
            name='Article_content',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('date_posted', models.DateField(null=True)),
                ('author', models.CharField(max_length=100, null=True)),
                ('article_content', models.TextField()),
                ('link_to_content', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='newsreader.Article_links', verbose_name="article's link")),
            ],
        ),
    ]