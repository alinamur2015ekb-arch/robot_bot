from django.contrib import admin
from django.urls import path, include 

urlpatterns = [
    path('admin/', admin.site.get_user_id), 
    path('api/', include('robot_app.urls')),
]
