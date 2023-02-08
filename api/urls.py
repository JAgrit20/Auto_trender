from django.urls import path
from . import views

urlpatterns = [
	path('', views.apiOverview, name="api-overview"),
	path('task-list/', views.taskList, name="task-list"),
	path('task-detail/<str:pk>/', views.taskDetail, name="task-detail"),
	path('task-create/', views.taskCreate_data, name="task-create"),
	path('task-create_5min/', views.taskCreate_data_5min, name="task-create_5min"),
	path('task-create_stocastic_up/', views.taskCreate_data_stocastic_up, name="task-create_stocastic_up"),
	path('task-create_stocastic_ADX/', views.taskCreate_data_stocastic_ADX, name="task-create_stocastic_ADX"),
	path('task-create_adx/', views.taskCreate_adx, name="task-create_adx"),
	path('task-create_rsi/', views.taskCreate_RSI, name="task-create_rsi"),
	path('taskCreate_ADX_5min/', views.taskCreate_ADX_5min, name="taskCreate_ADX_5min/"),
	path('task-create_nifty/', views.Nifty_Create, name="task-create_nifty"),
	path('task-update_nifty/', views.Nifty_Update, name="task-update_nifty"),
	path('task-update_nifty_exit/', views.Nifty_Create_exit, name="task-update_nifty_exit"),
	path('task-update/<str:pk>/', views.taskUpdate, name="task-update"),
	path('task-delete/<str:pk>/', views.taskDelete, name="task-delete"),
]
