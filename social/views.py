from django.shortcuts import render,redirect
from django.views.generic import ListView
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from social import models,forms

class Wall(LoginRequiredMixin, ListView):
    
    context_object_name='posts'
    template_name='social/wall.html'
    login_url='auth/login'
    
    def get_queryset(self):
#       return models.Post.objects.filter(user=self.request.user.pk)
        return models.Post.objects.filter(
            (Q(user__person1=self.request.user.pk) | Q(user__person2=self.request.user.pk)) &
            ~Q(user=self.request.user)
        )
    
        

#       return models.Post.objects.filter(user__in=friends)
class Home(LoginRequiredMixin,ListView):
    context_object_name='posts'
    template_name='social/home.html'
    login_url ='auth/login'

    def get_queryset(self):
        return models.Post.objects.filter(user=self.request.user.pk)
    def get_context_data(self,*args,**kwargs):
        data=super().get_context_data(*args,**kwargs)
        data['post_form']=forms.PostForm
        return data
class Post(View):
    def post(self,request):
        form=forms.PostForm(request.POST)
        if form.is_valid():
            post=form.save(commit=False)
            post.user=request.user
            post.save()
        
        return redirect('/home/')