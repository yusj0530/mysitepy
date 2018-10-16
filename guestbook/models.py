from django.db import models

# Create your models here.

class Guestbook(models.Model):

    name = models.CharField(max_length=100, default='')
    password = models.CharField(max_length=100, default='')
    content = models.CharField(max_length=200, default='')
    reg_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return 'guestbook( %s, %s, %s, %s)' %( self.name, self.password, self.content, self.reg_date)
