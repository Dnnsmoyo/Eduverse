# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, Client, RequestFactory
from myapp.models import Course
from django.contrib.auth.models import Group
import datetime
from django.utils.timezone import now
from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from myapp.views import CourseDetailView.get_context_data

# Create your tests here.
class CourseTestCase(TestCase):
    def test_course_model(self):
        course = Course.objects.create(name = 'devs' ,description="description")#,date_created= now())
        course.save()
        #self.assertEqual(comp.user ,'john')
        self.assertEqual(course.name ,'devs')
        self.assertEqual(course.description, "description")
        #self.assertEqual(course.date_created, now())
        
class PathTestCase(TestCase):
    def test_url_path(self):
        c = Client()
        client = APIClient()
        response = c.get('/courses')
        url_ = c.get('/course/(?P<pk>\d+)$')
        api = client.get('/api/?P<pk>\d+)$')
        url = c.get('/')
        url_.status_code
        api.status_code
        url.status_code
        response.status_code

class ViewTest(TestCase):
    def test_details(self):
        # Create an instance of a GET request.
        self.factory = RequestFactory() 
        request = self.factory.get('/course/1')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        #request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        #request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        #response = my_view(request)
        # Use this syntax for class-based views.
        #response = CourseDetailView.as_view()(request)
        response = get_context_data(request)
        self.assertEqual(response.status_code, 200)
