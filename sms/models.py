from django.db import models
from accounts.models import User 
# Create your models here.

class TextMessage(models.Model):
    receiver=models.CharField(max_length=50)
    message=models.TextField(max_length=400)
    date_added=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return  str(self.message)
    class Meta:
            verbose_name = ('Text Message')
            verbose_name_plural = ('Text Messages ' )


