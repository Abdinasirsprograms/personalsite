#!/sites/abdinasirnoor.com/.venv/bin/python3.6
import sys, os, mailbox
# sys.path.append('/sites/abdinasirnoor.com/src/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "personalsite.settings")
os.environ["DJANGO_SETTINGS_MODULE"] = 'personalsite.settings'
import django
django.setup()
from newsreader.pull_site_data import Site_data
from newsreader.pull_article_data import Article_data
from django.conf import settings
from django.core.management.base import BaseCommand
from landingpage.models import Inbox
from datetime import datetime

class Command(BaseCommand):
    help = 'Pull news site data'

    def handle(self, *args, **options):
        print('*'*100)
        print('\t\tExecuting Pull Site Data\n')
        Site_data()
        print('*'*100)

        print('*'*100)
        print('\t\tExecuting Pull Article Data\n')
        Article_data()
        print('*'*100)