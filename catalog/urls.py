from rest_framework.routers import DefaultRouter
from django.urls import path

from catalog.views import CatalogViewSet, load_data_view

router = DefaultRouter()
router.register('', CatalogViewSet, 'Catalog')

urlpatterns = router.urls

urlpatterns += [
    path('upload/data/', load_data_view, name='load_data')
]

