# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from myapp.models import Course, Profile
# Register your models here.
admin.site.register(Course)
admin.site.register(Profile)
