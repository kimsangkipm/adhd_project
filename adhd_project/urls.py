from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('apps.survey.urls')),  # ADHD 설문 앱 추가
]
