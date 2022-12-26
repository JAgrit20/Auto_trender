from django.urls import path
from . import views

urlpatterns = [
        path('', views.index, name='index'),
        path('s2', views.strategy_2, name='strategy_2'),
]
