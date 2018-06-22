# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from actstream import action
# Create your models here.
class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=200)
    date_created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', args=[str(self.id)])

    
def my_handler(sender, instance, created, **kwargs):
    action.send(instance, verb='was added')

post_save.connect(my_handler, sender=Course)

class Profile(models.Model):
    user =  models.OneToOneField('auth.User',null=True)
    photo = models.ImageField(upload_to='media')
    country = models.CharField(max_length=100)
    DOB = models.DateField()

    def __str__(self):
        return self.country
    
