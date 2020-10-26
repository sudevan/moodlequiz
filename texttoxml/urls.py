from django.urls import path
from . import views as texttoxml
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('',texttoxml.textToxmlConverterView.as_view(),name='home'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)