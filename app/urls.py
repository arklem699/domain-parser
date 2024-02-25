from django.contrib import admin
from domain_parser import views
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.hello),
    path('download/', views.download, name='download'),
]
