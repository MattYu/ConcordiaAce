"""ace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from view import home_page
from joblistings.views import job_details, post_job, download_jobPDF
from jobapplications.views import add_resume, download_test, browse_job_applications, concatinate_applicationPDF, get_protected_file
from accounts.views import register_user, logout_user, login_user, activate
from django.urls import include

urlpatterns = [
    path('', home_page),
    path('admin/', admin.site.urls),
    path('job-details/<int:pk>/', job_details),
    path('employer-dashboard-post-job/', post_job),
    path('add-resume/<int:pk>/', add_resume),
    path('tinymce', include('tinymce.urls')),
    path('test/<int:pk>/', download_test),
    path('jobDescription/<int:pk>/', download_jobPDF),
    path('register/', register_user),
    path('logout/', logout_user),
    path('login/', login_user),
    path('activate/<uidb64>/<token>', activate, name="activate"),
    path('jobApplications/', browse_job_applications),
    #path('applicationDetails/<int:pk>/', ),
    path('concatinateApplications/', concatinate_applicationPDF),
    path('getFile/<str:uid>/<str:candidateId>/<str:filetype>/<str:fileid>/<token>/', get_protected_file),
]

if settings.DEBUG:
    urlpatterns = urlpatterns + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
