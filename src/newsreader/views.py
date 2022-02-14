import json
import logging
import re

from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_http_methods

from newsreader.pull_site_data import requestWebsite

from .models import Article_links, Article_site

logging.basicConfig(level=logging.DEBUG) # Here




class websiteConsumer(AsyncJsonWebsocketConsumer):
        def __init__(self, *args, **kwargs):
            self.sessionID = ''
            self.requestObjectCreated = False
            super().__init__(*args, **kwargs)

        def websocket_connect(self, message):
                print('Accpeting connection...')
                return self.accept()


        async def websocket_receive(self, message):
                url = message.get('text').strip()
                close_connection = bool(url == 'CLOSE_CONNECTION')

                if close_connection: return await self.closeConnection()

                url_is_empty = bool(len(url) == 0)
                if url_is_empty: 
                        await self.send_json('Error, empty URL recieved!')
                        return  await self.closeConnection(3000) 
                else:
                        if self.startEngine(url) == False: 
                                await self.send_json('start Engine Failure!')
                                return await close_connection(3000)
                        else:
                                response = self.getContent()
                                if response == False: 
                                        await self.send_json('start Engine Failure!')
                                        return await close_connection(3000)
                                else:
                                        return await self.send_json(response)

        def startEngine(self, url):        
                self.requestObj = requestWebsite()
                self.requestObj.startEngine(url)

        def getContent(self):
                return self.requestObj.getPage()

        async def closeConnection(self, code=1000):
                await self.send_json('closing connection....')
                try:
                        self.requestObj.shutDown()
                except AttributeError:
                        # this is to avoid a race condition in case requestObj hasn't been created
                        self.send_json("Engine wasn't started properly!!")
                        pass
                return await self.close(code)    

        def websocket_disconnect(self, code):
                print('Disconnecting...')



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


def start_site_request(request, site_url):
        # site_retrieved = requestWebsite(site_url)
        return JsonResponse(request, {'site_retrived':site_url})


@require_http_methods(['POST'])
def return_proxy(request):
        try:
                received_data = json.loads(request.body)
                site_url = received_data.get('site_url')
                if site_url is None: raise ValueError
                # startSite = start_site_request(request, site_url)
                # TODO:
                # setup the pulling site data
                # then injecting vite assets                
                # return JsonResponse({'site_url': True, 'returned_info': startSite}, safe=False, headers={'Access-Control-Allow-Origin':'*'})
                return start_site_request(request, site_url)

        except ValueError:
                logging.error(f'\n!!! \nPOST data is empty: {received_data}\n!!!')
                return JsonResponse({'receivedValue': received_data}, status="400")
        
        except Exception as e:
                logging.error(f'failed for unknown reason: ')
                data = {'unkown failure':f'{e}','receivedValue': received_data}
                return JsonResponse(data, status="500", safe=False)

