from django.urls import path
from . import views

urlpatterns = [
	path('', views.apiOverview, name="api-overview"),
	path('task-list/', views.taskList, name="task-list"),
	path('task-detail/<str:pk>/', views.taskDetail, name="task-detail"),
	path('task-create/', views.taskCreate, name="task-create"),
	path('task-create_rsi/', views.taskCreate_RSI, name="task-create_rsi"),
	# path('taskCreate_adx/', views.taskCreate, name="task-create"),
	# path('task-create_adx/', views.taskCreate_ADX, name="task-create_adx"),
	path('task-create_nifty/', views.Nifty_Create, name="task-create_nifty"),
	path('task-update_nifty/', views.Nifty_Update, name="task-update_nifty"),
	path('task-update_nifty_exit/', views.Nifty_Create_exit, name="task-update_nifty_exit"),

	path('task-update/<str:pk>/', views.taskUpdate, name="task-update"),
	path('task-delete/<str:pk>/', views.taskDelete, name="task-delete"),
]
