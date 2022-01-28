from turtle import title
from django.shortcuts import redirect
from django.forms import forms
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView , UpdateView , DeleteView , FormView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from .models import task
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class CustomLoginView(LoginView):
    template_name ='base/login.html' 
    fields = '__all__'   
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task-list')

class Registerpage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('task-list')

    def form_valid(self, form): 
        user= form.save()
        if user is not None:
            login(self.request, user)
        return super(Registerpage, self).form_valid(form)
   
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
           return redirect('task-list')
        return super(Registerpage, self).get(*args, **kwargs) 


class TaskList(LoginRequiredMixin,ListView):
    model = task
    context_object_name ='task_l'   # used this to replace object_list in template(task_list.html) by task_l
    
    def get_context_data(self, **kwargs):
            context = super().get_context_data(**kwargs)
            context['task_l'] = context['task_l'].filter(user=self.request.user)
            context['count'] = context['task_l'].filter(complete = False).count()
            
            search_input = self.request.GET.get('search-area') or ''

            if search_input:
                context['task_l'] = context['task_l'].filter(title__startswith = search_input)

            context['search_input'] = search_input
            return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model = task    
    context_object_name ='task_d'   # used this to replace object in template(task_detail.html) by task_d

    # template_name = 'base/task.html' # we used this to change the name of html file task_detail.html to task.html (if you don't use it then this class will automatically search for task_detail.html)


class TaskCreate(LoginRequiredMixin,CreateView):
    model = task     
    fields = ['title','description','complete']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form): 
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = task
    fields = ['title','description','complete']
    template_name = 'base/taskupdate_form.html'
    success_url = reverse_lazy('task-list')


class TaskDelete(LoginRequiredMixin,DeleteView):
    model = task
    context_object_name ='task_delete'
    success_url = reverse_lazy('task-list')


