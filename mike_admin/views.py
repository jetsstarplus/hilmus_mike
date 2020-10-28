from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView, RedirectView
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model

from .models import Music

from .forms import ProfileForm


def home(request):
    return render(request, template_name='mike_admin/dashboard-2.html', context={} )

def profile(request):
    profile=None
    if request.user.is_authenticated:
        profile = get_object_or_404(get_user_model(), pk=request.user.pk)
        musics = Music.objects.filter(artist=request.user.pk).all()
        boomplay= Music.objects.filter(artist=request.user.pk, is_sent=True).count()
        music_number= musics.count()
        
    else:
        profile=None
    context={
        'profile': profile, 
        'musics': musics, 
        'music_number':music_number,
        'boomplay':boomplay,
        }
    return render(request, template_name="mike_admin/profile.html", context=context)

class UserListView(ListView):
    models=get_user_model()
    template_name='mike_admin/profile.html'
    context_object_name='user_list'

class UpdateProfileView(UpdateView):
    model= settings.AUTH_USER_MODEL
    template_name = 'mike_admin/profile.html'
    form_class= ProfileForm
    
    def get_object(self, *args, **kwargs):
        user = get_object_or_404(settings.AUTH_USER_MODEL, pk=self.kwargs['pk'])

        # We can also get user object using self.request.user  but that doesnt work
        # for other models.

        return user.userprofile

    def get_success_url(self, *args, **kwargs):
        return reverse("profile")
# Create your views here.
