"""provisioning URL Configuration

Defined URLS are
'/admin/provApp/form/<id>' -> PresentXMLDataView
'/admin/' -> admin.site.urls
'/api/' -> provApp.urls
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from provApp.views import PresentXMLDataView


urlpatterns = [
    path('admin/provApp/form/<id>',
         PresentXMLDataView.as_view(), name="xmldata"),
    path('admin/', admin.site.urls),
    path('api/', include('provApp.urls')),

]
