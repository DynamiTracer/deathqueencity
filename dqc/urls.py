from django.urls import path
from . import views

#app_name = 'dqc'

urlpatterns = [
    path('', views.IndexView.as_view()),
    path('index/', views.IndexView.as_view()),
    path('soft/<int:pk>/',views.SoftView.as_view(), name='softdetail'),    
    path('category/<int:pk>/', views.CategoryView.as_view(), name='categorydetail'),
    path('special/<int:pk>/', views.SpecialView.as_view(), name='specialdetail'),
    path('history/', views.HistoryView.as_view()),
    path('wanted/', views.WantedView.as_view()),
]