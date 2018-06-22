# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from allauth.account.views import SignupView, LoginView, LogoutView
from django.views.generic.edit import CreateView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from myapp.forms import CourseForm, ProfileForm
from django.utils import timezone
from myapp.models import Course, Profile
from django.contrib.auth.models import Group
from .serializers import CourseSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from actstream.models import Action
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.decorators.csrf import csrf_exempt
from ws4redis.redis_store import RedisMessage
from ws4redis.publisher import RedisPublisher
# Create your views here.

def homeview(request):
    course = Course.objects.all()
    act = Action.objects.all()
    c = Action.objects.count()
    return render(request,'index.html',{'course':course,'act':act,'c':c})

class CourseListView(ListView):
    template_name='course_list.html'
    model = Course
    
    def get_context_data(self, **kwargs):
        context = super(CourseListView,self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
    
class CourseDetailView(DetailView):
    template_name='myapp/course_detail.html'
    model = Group
    #context_object_name = 'course_object'

    def get_context_data(self, **kwargs):
        context = super(CourseDetailView,self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
    
class ProfileFormView(CreateView):
    template_name= 'profile_form.html'
    form_class = ProfileForm
    success_url ='/'
    
class ProfileDetailView(DetailView):
    #template_name='profile_detail.html'
    model = Profile

    
class CourseList(APIView):
    """
    List all Courses, or create a new Course.
    """
    def get(self, request, format=None):
        courses = Course.objects.all()
        serializer = CourseSerializer(courses, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CourseDetail(APIView):
    """
    Retrieve, update or delete a Course instance.
    """
    def get_object(self, pk):
        try:
            return Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        Course = self.get_object(pk)
        serializer = CourseSerializer(Course)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        Course = self.get_object(pk)
        serializer = CourseSerializer(Course, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        Course = self.get_object(pk)
        Course.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class SignupView(SignupView):
    template_name = 'accounts/signup.html'


class LoginView(LoginView):
    template_name = 'accounts/login.html'


class LogoutView(LogoutView):
    template_name = 'accounts/logout.html'

class CourseFormView(CreateView):
    template_name = 'course_form.html'
    form_class = CourseForm()
    success_url = 'detail'

class BroadcastChatView(TemplateView):
    template_name = 'broadcast_chat.html'

    def get(self, request, *args, **kwargs):
        welcome = RedisMessage('Hello everybody')  # create a welcome message to be sent to everybody
        RedisPublisher(facility='foobar', broadcast=True).publish_message(welcome)
        return super(BroadcastChatView, self).get(request, *args, **kwargs)

    def profiles(request):
        pros = Profile.objects.filter(user=request.user)
        return render(request,template_name,{'pros':pros})


class UserChatView(TemplateView):
    template_name = 'user_chat.html'

    def get_context_data(self, **kwargs):
        context = super(UserChatView, self).get_context_data(**kwargs)
        context.update(users=User.objects.all())
        return context

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(UserChatView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        redis_publisher = RedisPublisher(facility='foobar', users=[request.POST.get('user')])
        message = RedisMessage(request.POST.get('message'))
        redis_publisher.publish_message(message)
        return HttpResponse('OK')


class GroupChatView(TemplateView):
    template_name = 'group_chat.html'

    def get_context_data(self, **kwargs):
        context = super(GroupChatView, self).get_context_data(**kwargs)
        context.update(groups=Group.objects.all())
        return context

    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(GroupChatView, self).dispatch(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        redis_publisher = RedisPublisher(facility='foobar', groups=[request.POST.get('group')])
        message = RedisMessage(request.POST.get('message'))
        redis_publisher.publish_message(message)
        return HttpResponse('OK')
    
