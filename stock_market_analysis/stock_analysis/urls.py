from django.urls import path
from . import views

urlpatterns = [
    path('upload/', views.upload_stock_data, name='upload'),
    path('analyze/', views.analyze_stock_data, name='analyze_stock_data'),
    
]
