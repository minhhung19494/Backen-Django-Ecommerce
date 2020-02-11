from django.db import models
from core.models import UserProfile

# Create your models here.


class CrawlInfo(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    last_scrape = models.DateTimeField(null=True, blank=True)
