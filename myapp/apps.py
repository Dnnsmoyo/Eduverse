# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig,apps


class MyappConfig(AppConfig):
    name = 'myapp'

    def ready(self):
        from actstream import registry
        registry.register(self.get_model('Course'),apps.get_model('auth','User')),
