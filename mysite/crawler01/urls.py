from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # path('test', views.showtemplate),
    # path('test', views.tasks_index, name="tasks_index"),
    path('detail', views.tasks_index, name="tasks_index"),
    path('create', views.tasks_create_view, name="tasks_create"),
    path('create2', views.tasks_create2_view, name="tasks_create2"),
]