from datetime import timedelta, timezone, datetime
from .models import CrawlInfo
from core.models import Item, UserProfile
from home.storage_backends import MediaStorage
from bs4 import BeautifulSoup
from django.shortcuts import render, redirect
from django.conf import settings
import requests
import shutil
import os
requests.packages.urllib3.disable_warnings()


def scrape(request):
    user_p = UserProfile.objects.filter(user=request.user).first()
    scrapeTime = datetime.now(timezone.utc)
    crawlInfo = CrawlInfo.objects.create(user=user_p, last_scrape=scrapeTime)

    session = requests.Session()
    session.headers = {
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}
    url = "https://bitis.com.vn/collections/nam"
    content = session.get(url, verify=False).content
    soup = BeautifulSoup(content, "html.parser")
    items = soup.find_all(
        'div', {'class': 'product-lists-item'})  # list of item

    for item in items:
        name = item.find_all('h3', {'class': 'product_name'})[0].a.text
        imgSource = 'http:' + item.find('img', {'class': 'image_main'})['src']
        print(imgSource)
        category = item.find_all(
            'div', {'class': 'product_category'})[0].a.text

# stackover flow solution
        media_root = settings.MEDIA_ROOT
        media_storage = MediaStorage()
        if not imgSource.startswith(("data:image", "javascript")):
            local_filename = imgSource.split('/')[-1].split("?")[0]
            r = session.get(imgSource, stream=True, verify=False)
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=1024):
                    f.write(chunk)
            current_image_absolute_path = os.path.abspath(local_filename)
            shutil.move(current_image_absolute_path, media_root)
# end solution

#aws S3 upload
        media_storage.save(local_filename, file_obj)
        file_url = media_storage.url(local_filename)
#end solution

        new_Item = Item()
        new_Item.title = name
        new_Item.image = local_filename
        new_Item.category = category
        new_Item.save()

    return redirect('/')
