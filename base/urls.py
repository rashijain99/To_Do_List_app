from django import views
from django.urls import path 
from .views import TaskList , TaskDetail , TaskCreate, TaskUpdate, TaskDelete , CustomLoginView , Registerpage
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', TaskList.as_view(), name='task-list'),
    path('task/<int:pk>/', TaskDetail.as_view(),  name='task-detail'),
    path('create_task', TaskCreate.as_view(), name='task-create'),
    path('update_task/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('delete_task/<int:pk>/', TaskDelete.as_view(), name='task-delete'),

    path('login/', CustomLoginView.as_view() , name='login'),
    path('logout/', LogoutView.as_view(next_page='login') , name='logout'),
    path('register/' , Registerpage.as_view() , name='register')
]

