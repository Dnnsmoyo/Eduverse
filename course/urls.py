"""course URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from myapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$',views.homeview,name='home'),
    url(r'^chat/$', views.BroadcastChatView.as_view(), name='broadcast_chat'),
    url(r'^userchat/$', views.UserChatView.as_view(), name='user_chat'),
    url(r'^groupchat/$', views.GroupChatView.as_view(), name='group_chat'),
    url(r'^new-profile/$',views.ProfileFormView.as_view(),name='profile_form'),
    url(r'^profile/(?P<pk>\d+)$',views.ProfileDetailView.as_view(),name='profile_detail'),
    url(r'^api$',views.CourseList.as_view(),name='api'),
    url(r'^api/(?P<pk>\d+)$',views.CourseDetail.as_view(),name='course-detail'),
    url(r'^courses$',views.CourseListView.as_view(),name="courses"),
    url(r'^course/(?P<pk>\d+)$',views.CourseDetailView.as_view(template_name='myapp/course_detail.html'),name='detail'), 
    url(r'^signup',views.SignupView.as_view(),name='signup'),
    url(r'^login',views.LoginView.as_view(),name='login'),
    url(r'^logout',views.LogoutView.as_view(),name='logout'),
    url(r'^accounts/',include('allauth.urls')),
    url(r'^activity/',include('actstream.urls')),
    url(r'^admin/', admin.site.urls),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
