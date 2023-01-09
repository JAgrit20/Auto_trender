from django.urls import path,include
from . import views
# from counter_api import urls as todo_urls

urlpatterns = [
        path('', views.index, name='index'),
        path('s2', views.strategy_2, name='strategy_2'),
        path('check', views.Check, name='check'),
        # path('todos/', include(todo_urls)),
]
