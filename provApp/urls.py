"""
Define URL for application provApp. On the project side all of the URLs define here are under /API/.

URLs here are for REST API:
'/api/devvendor/' -> DevVendorViewSet
'/api/devmodel/' -> DevModelViewSet
'/api/device/' -> DeviceViewSet
'/api/customer/' -> CustomerViewSet
'/api/extension/' -> ExtensionViewSet
'/api/dss/' -> DSSViewSet
'/api/xml/' -> GetXMLConfigEndpoint

"""
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from .views import DevVendorViewSet, DevModelViewSet, DeviceViewSet, CustomerViewSet, ExtensionViewSet, DSSViewSet
from .endpoints import GetXMLConfiguration

router = routers.DefaultRouter()
router.register('devvendor', DevVendorViewSet)
router.register('devmodel', DevModelViewSet)
router.register('device', DeviceViewSet)
router.register('customer', CustomerViewSet)
router.register('extension', ExtensionViewSet)
router.register('dss', DSSViewSet)


urlpatterns = [

    path('', include(router.urls)),
    path('xml/', GetXMLConfiguration.as_view(), name="GetXMLConfigEndpoint")

]
