from django.urls import path
from . import views

urlpatterns = [
	
	path('',
		views.transformer_list,
		name = 'employee-list1'),
	path('transformers/',
		views.transformer_list,
		name = 'employee-list'),
	path('transformers/<int:pk>/',
		views.transformer_detail,
		name = 'employee-detail'),
]
