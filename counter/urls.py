from django.urls import path,include
from . import views
# from counter_api import urls as todo_urls

urlpatterns = [
        path('', views.index, name='index'),
        path('s2', views.strategy_2, name='strategy_2'),
        path('check', views.Check, name='check'),
        path('check_both', views.Check_both, name='check'),
        # path('check_adx', views.check_adx, name='check_adx'),
        path('api/', include('api.urls')),
]
