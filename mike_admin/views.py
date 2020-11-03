from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView, RedirectView
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Music
from article.models import Post

from .forms import ProfileForm

@login_required
def home(request):    
    return render(request, template_name='mike_admin/dashboard-2.html', context={} )

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

    

# class UpdateProfileView(UpdateView):
#     model= settings.AUTH_USER_MODEL
#     template_name = 'mike_admin/profiles/update_profile.html'
#     form_class= ProfileForm
    
#     def get_object(self, *args, **kwargs):
#         user = get_object_or_404(get_user_model(), pk=self.request.user.pk)

#         # We can also get user object using self.request.user  but that doesnt work
#         # for other models.

#         return user

#     def get_success_url(self, *args, **kwargs):
        # return reverse("mike_admin:profile")
# Create your views here.
