from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView, RedirectView
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from datetime import datetime, timedelta
from django.utils import timezone
from django.views import generic

from .models import Music, Testimonial, StaffMember
from article.models import Post

from .forms import ProfileForm, TestimonialForm, TermsForm, StaffMemberForm

@login_required
def home(request): 
    user_music=Music.objects.filter(artist=request.user).order_by('-date_added')
    users=None
    musics=None
    testimonials=None
    new_users=0
    user_percentage=0
    if request.user.is_staff:
        
        users=get_user_model().objects.filter(is_active=True).order_by('-date_joined')
        musics=Music.objects.filter(is_sent=False).order_by('-date_added')
        # Checking for new users of the system
        for user in users:
            if timezone.now() - user.date_joined <= timedelta(days=30):
                new_users +=1
        user_percentage=(new_users/int(users.count()))   
        testimonials= Testimonial.objects.filter(is_published=True).order_by('-date_added')
        upload=Music.objects.filter(is_sent=True).order_by('-date_added')
        
    
    context={
        'user_music':user_music,
        'users':users,
        'musics':musics,
        'testimonials':testimonials,
        'new_users':new_users,
        'user_percentage':user_percentage,
        'upload':upload
    }
    return render(request, template_name='mike_admin/dashboard-2.html', context=context )

@login_required
def profile(request):
    profile=None
    if request.user.is_authenticated:
        profile = get_object_or_404(get_user_model(), pk=request.user.pk)
        musics = Music.objects.filter(artist=request.user.pk).all()
        boomplay= Music.objects.filter(artist=request.user.pk, is_sent=True).count()
        music_number= musics.count()
        articles = Post.objects.filter(author=request.user.pk, status=1)
        
    else:
        profile=None
    context={
        'profile': profile, 
        'musics': musics, 
        'music_number':music_number,
        'boomplay':boomplay,
        'article':articles
        }
    return render(request, template_name="mike_admin/profiles/profile.html", context=context)

class UserListView(ListView, LoginRequiredMixin):
    models=get_user_model()
    template_name='mike_admin/profiles/profile.html'
    context_object_name='user_list'
    paginate_by = 20

@login_required
def update_profile(request):
    user = request.user
    error= None
    message=None
    form=None
    template_name = 'mike_admin/profiles/update_profile.html'
    # user=request.user
   
    if request.method=='POST':
            form = ProfileForm(request.POST, request.FILES, instance=user)
            # user=user.save( commit=False) 
            if form.is_valid():    
                try:                        
                    form.save()                    
                    message="Your profile was successfully updated"
                except:
                    error="There was a problem with your submission"
            else:
                error="There a problem with your submission"
    else:
        form= ProfileForm(instance=user)
    
    context={
        'user':user,
        'form':form,
        'error': error,
        'message': message
        }
    return render(request, template_name, context=context)


# The testimonial controllers
class TestimonialList(generic.ListView, LoginRequiredMixin):
    queryset = Testimonial.objects.filter(is_published=True).order_by('-date_added')
    template_name = 'mike_admin/testimonials/index.html'
    paginate_by=10

@login_required
def create_testimonial(request):
    template_name='mike_admin/testimonials/create_testimonial.html'
    new_post=None
    error=None
    slug=None
    user=request.user
    
    if user.is_staff:   
        if request.method=='POST':
            form = TestimonialForm(request.POST, request.FILES)
            if form.is_valid():
               
                new_post= form.save(commit=False)
                new_post.added_by= request.user
                new_post.save()
            else:
                error="There was a problem with your submission"
        else:
            form= TestimonialForm()
    
    context={
        'user':user,
        'new_post':new_post,
        'form':form,
        'slug':slug,
        'error':error
        }
    return render(request, template_name, context=context)

@login_required
def update_testimonial(request, id):
    template_name='mike_admin/testimonials/edit_testimonial.html'
    post = get_object_or_404(Testimonial, pk=id)
    error=None
    user=request.user
    id=None
    message=None
    
    if user.is_staff:   
        if request.method=='POST':
            form = TestimonialForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                try:  
                    form.save()         
                    # post=post.update(post=form.cleaned_data['post'], status=form.cleaned_data['status'])
                    id=post.id
                    message="Post Update successful"
                except:
                    error="There was a problem with your submission"
            else:
                error = "Your data is not complete"
        else:
            form= TestimonialForm(instance=post)
    
    context={
        'user':user,
        'post':post,
        'form':form,
        'id': id,
        'error': error,
        'message':message,
        }
    return render(request, template_name, context=context)

@login_required
def delete_testimonial(request, id):
    template_name='mike_admin/testimonials/confirm_delete.html'
    final_template='mike_admin/testimonials/delete_testimonial.html'
    post= get_object_or_404(Testimonial, id=id)
    error=None
    user=request.user
    slug=None
    message= None
    
    if user.is_staff:   
        if request.method=='POST':
            if request.user == post.author:                           
                    post=post.delete()
                    message="The post has been successfully deleted"                   
            else:
                error ="You are not authorized to edit this post"   
                
            return render(request, final_template, {'post': post})    
                    
        else:
            
            form= TestimonialForm(instance=post)
    
    context={
        'user':user,
        'post':post,
        'form':form,
        'id': id,
        'error': error,
        'message':message
        }
    return render(request, template_name, context=context)
    
@login_required
def testimonial_detail(request, id):
    template_name = 'mike_admin/testimonials/testimonial_detail.html'
    post = get_object_or_404(Testimonial, pk=id)     # Comment posted
    
    context = {
        'post': post
    }
    return render(request, template_name, context=context)