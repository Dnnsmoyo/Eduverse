from django.forms import ModelForm
from myapp.models import Course, Profile

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = '__all__'
        
class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['photo','country','DOB']
