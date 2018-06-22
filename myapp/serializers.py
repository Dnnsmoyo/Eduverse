from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import Group, User
from myapp.models import Course

class CourseSerializer(ModelSerializer):
        view_name='course-detail',
        lookup_field='pk',
        many=True,
        read_only=True
	class Meta:
		model = Course
		fields = '__all__'
