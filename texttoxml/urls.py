from django.urls import path
from . import views as texttoxml

urlpatterns = [
    path('',texttoxml.textToxmlConverterView.as_view(),name='home'),
]