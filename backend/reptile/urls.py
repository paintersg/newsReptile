from django.urls import path

from . import views

urlpatterns = [
    path('gzdaily/', views.gzdaily, name='gzdaily'),
    path('huxiu/', views.huxiu, name='huxiu'),
    path('results/', views.results, name='results'),
]
