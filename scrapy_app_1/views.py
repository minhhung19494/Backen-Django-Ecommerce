from scrapyd_api import ScrapydAPI
from django.http import JsonResponse

def crawl(request):
    scrapyd = ScrapydAPI('http://localhost:6800')
    url = 'https://bitis.com.vn/collections/hunter-nam/'
    url = url
    settings = {
                'USER_AGENT': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'
            }
    task = scrapyd.schedule('default', 'icrawler', 
                settings=settings, )
    return JsonResponse({'status': 'started'})