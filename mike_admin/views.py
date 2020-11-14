from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView, RedirectView
from django.conf import settings
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import datetime, timedelta
from django.utils import timezone
from django.views import generic
from django.contrib import messages
from django.http import HttpResponse

from .models import Music, Testimonial, StaffMember, TermsOfService
from article.models import Post
from daraja.models import Lipa_na_mpesa, C2BPaymentModel, Initiate

from .forms import ProfileForm, TestimonialForm, TermsForm, StaffMemberForm, MusicForm

@login_required
def home(request): 
    user_music=Music.objects.filter(artist=request.user).order_by('-date_added')
    users=None
    musics=None
    testimonials=None
    new_users=0
    user_percentage=0
    lipa_transactions=None
    inactive_users=None
    if request.user.is_staff:
        if request.user.get_full_name()==None:             
            messages.add_message(request, messages.WARNING,  "Please Ensure You Complete Your Profile")  
           
        users=get_user_model().objects.filter(is_active=True).order_by('-date_joined')
        inactive_users = get_user_model().objects.filter(is_active=False).order_by('-date_joined')
        musics=Music.objects.filter(is_sent=False).order_by('-date_added')
        # Checking for new users of the system
        for user in users:
            if timezone.now() - user.date_joined <= timedelta(days=30):
                new_users +=1
        user_percentage=(new_users/int(users.count()))   
        testimonials= Testimonial.objects.filter(is_published=True).order_by('-date_added')
        upload=Music.objects.filter(is_sent=True).order_by('-date_added')
        lipa_transactions=Lipa_na_mpesa.objects.all().order_by('-TransationDate')
    
    elif request.user:
        if request.user.is_payed==False:            
            messages.add_message(request, messages.INFO,  "Please Complete Your Payment First Inorder To Proceed")
        if request.user.first_name==None or request.user.last_name==None or request.user.avatar==None:             
            messages.add_message(request, messages.WARNING,  "Please Ensure You Complete Your Profile")  
                
        musics=Music.objects.filter(artist=request.user, is_sent=False).order_by('-date_added') 
        upload=Music.objects.filter(artist=request.user, is_sent=True).order_by('-date_added') 
    
    context={
        'user_music':user_music,
        'users':users,
        'musics':musics,
        'testimonials':testimonials,
        'new_users':new_users,
        'user_percentage':user_percentage,
        'upload':upload,
        'inactive_users':inactive_users,
        'lipa_transactions':lipa_transactions,
    }
    return render(request, template_name='mike_admin/dashboard-2.html', context=context )

@login_required
def profile(request):
    profile=None
    if request.user.is_authenticated:
        profile = get_object_or_404(get_user_model(), pk=request.user.pk)
        musics = Music.objects.filter(artist=request.user.pk).all()
        boomplay= Music.objects.filter(artist=request.user.pk, is_boompay=True).count()
        music_number= musics.count()
        articles = Post.objects.filter(author=request.user.pk, status=1)
        skiza=Music.objects.filter(artist=request.user.pk, is_skiza=True).count()
        transactions=Initiate.objects.filter(ResultCode=1, user=request.user)
                
    else:
        profile=None
    context={
        'profile': profile, 
        'musics': musics, 
        'music_number':music_number,
        'boomplay':boomplay,
        'article':articles,
        'skiza': skiza,
        'transactions':transactions
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
class TestimonialList(generic.ListView, LoginRequiredMixin, UserPassesTestMixin):
    queryset = Testimonial.objects.filter(is_published=True).order_by('-date_added')
    template_name = 'mike_admin/testimonials/index.html'
    context_object_name='testimonials'
    paginate_by=10
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    

@login_required
@user_passes_test(lambda user: user.is_staff)
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
@user_passes_test(lambda user: user.is_staff)
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
                    message="Testimonials Update successful"
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
@user_passes_test(lambda user: user.is_staff)
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
                    message="The testimonial has been successfully deleted"                   
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
@user_passes_test(lambda user: user.is_staff)
def testimonial_detail(request, id):
    template_name = 'mike_admin/testimonials/testimonial_detail.html'
    post = get_object_or_404(Testimonial, pk=id)     # Comment posted
    
    context = {
        'post': post
    }
    return render(request, template_name, context=context)

# The Staff Members controllers
class StaffList(generic.ListView, LoginRequiredMixin, UserPassesTestMixin):
    queryset = StaffMember.objects.filter(is_published=True).order_by('-rank')
    template_name = 'mike_admin/staff/index.html'
    context_object_name='staffs'
    paginate_by=10
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

@login_required
@user_passes_test(lambda user: user.is_staff)
def create_staff(request):
    template_name='mike_admin/staff/create_staff.html'
    new_post=None
    error=None
    id=None
    user=request.user
    
    if user.is_staff:   
        if request.method=='POST':
            form = StaffMemberForm(request.POST, request.FILES)
            if form.is_valid():
               new_post =form.save()
               id= new_post.id
            else:
                error="There was a problem with your submission"
        else:
            form= StaffMemberForm()
    
    context={
        'user':user,
        'new_post':new_post,
        'form':form,
        'id':id,
        'error':error
        }
    return render(request, template_name, context=context)

@login_required
@user_passes_test(lambda user: user.is_staff)
def update_staff(request, id):
    template_name='mike_admin/staff/edit_staff.html'
    post = get_object_or_404(StaffMember, pk=id)
    error=None
    user=request.user
    id=None
    message=None
    
    if user.is_staff:   
        if request.method=='POST':
            form = StaffMemberForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                try:  
                    form.save()         
                    # post=post.update(post=form.cleaned_data['post'], status=form.cleaned_data['status'])
                    id=post.id
                    message="Staff Update successful"
                except:
                    error="There was a problem with your submission"
            else:
                error = "Your data is not complete"
        else:
            form= StaffMemberForm(instance=post)
    
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
@user_passes_test(lambda user: user.is_staff)
def delete_staff(request, id):
    template_name='mike_admin/staff/confirm_delete.html'
    final_template='mike_admin/staff/delete_staff.html'
    post= get_object_or_404(StaffMember, id=id)
    error=None
    user=request.user
    id=None
    message= None
    
    if user.is_staff:   
        if request.method=='POST':
            if request.user:                           
                    post=post.delete()
                    message="The staff member has been successfully deleted"  
                    id=post.id                 
            else:
                error ="You are not authorized to edit this staff"   
                
            return render(request, final_template, {'post': post})    
                    
        else:
            
            form= StaffMemberForm(instance=post)
    
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
@user_passes_test(lambda user: user.is_staff)
def staff_detail(request, id):
    template_name = 'mike_admin/staff/staff_detail.html'
    post = get_object_or_404(Testimonial, pk=id)     # Comment posted
    
    context = {
        'post': post
    }
    return render(request, template_name, context=context)

# The Tos controllers
class TermsList(generic.ListView, LoginRequiredMixin, UserPassesTestMixin):
    queryset = TermsOfService.objects.all().order_by('-date_added')
    template_name = 'mike_admin/terms/index.html'
    context_object_name= "terms"
    paginate_by=10
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

@login_required
@user_passes_test(lambda user: user.is_staff)
def create_terms(request):
    template_name='mike_admin/terms/create_terms.html'
    new_post=None
    error=None
    id=None
    user=request.user
    
    if user.is_staff:   
        if request.method=='POST':
            form = TermsForm(request.POST)
            if form.is_valid():
               new_post= form.save()
               id= new_post.id
            else:
                error="There was a problem with your submission"
        else:
            form= TermsForm()
    
    context={
        'user':user,
        'new_post':new_post,
        'form':form,
        'id':id,
        'error':error
        }
    return render(request, template_name, context=context)

@login_required
@user_passes_test(lambda user: user.is_staff)
def update_terms(request, id):
    template_name='mike_admin/terms/edit_terms.html'
    terms = get_object_or_404(TermsOfService, pk=id)
    error=None
    user=request.user
    id=None
    message=None
    
    if user.is_staff:   
        if request.method=='POST':
            form = TermsForm(request.POST, instance=terms)
            if form.is_valid():
                try:  
                    terms = form.save()         
                    # post=post.update(post=form.cleaned_data['post'], status=form.cleaned_data['status'])
                    id=terms.id
                    message="Terms Update successful"
                except:
                    error="There was a problem with your submission"
            else:
                error = "Your data is not complete"
        else:
            form= TermsForm(instance=terms)
    
    context={
        'user':user,
        'terms':terms,
        'form':form,
        'id': id,
        'error': error,
        'message':message,
        }
    return render(request, template_name, context=context)

@login_required
@user_passes_test(lambda user: user.is_staff)
def delete_terms(request, id):
    template_name='mike_admin/terms/confirm_delete.html'
    final_template='mike_admin/terms/delete_terms.html'
    post= get_object_or_404(TermsOfService, id=id)
    error=None
    user=request.user
    id=None
    message= None
    
    if user.is_staff:   
        if request.method=='POST':
            if request.user:                           
                    post=post.delete()
                    message="The term of service has been successfully deleted"                   
            else:
                error ="You are not authorized to edit this page"   
                
            return render(request, final_template, {'post': post})    
                    
        else:
            
            form= TermsForm(instance=post)
    
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
def terms_detail(request, id):
    template_name = 'mike_admin/terms/terms_detail.html'
    post = get_object_or_404(TermsOfService, pk=id)     # Comment posted
    
    context = {
        'post': post
    }
    return render(request, template_name, context=context)

# The Tos controllers
class MusicList(generic.ListView, LoginRequiredMixin):
    queryset = Music.objects.all().order_by('-date_added')
    template_name = 'mike_admin/music/index.html'
    context_object_name= "musics"

@login_required
def create_music(request, **kwargs):
    template_name='mike_admin/music/create_music.html'
    new_post=None
    error=None
    id=None
    user=request.user
    form=None
    
    if user.is_payed or user.is_staff:   
        if request.method=='POST':
            form = MusicForm(request.POST, request.FILES)
            if form.is_valid():
               new_post= form.save(commit=False)
               new_post.artist= user
               new_post.save()
               id= new_post.pk
            else:
                error="There was a problem with your submission"
        else:
            form= MusicForm()
    else:
        error="Please Complete the payment first"
    
    context={
        'user':user,
        'new_post':new_post,
        'form':form,
        'id':id,
        'error':error
        }
    return render(request, template_name, context=context)

@login_required
def update_music(request, pk, **kwargs):
    template_name='mike_admin/music/edit_music.html'
    music = get_object_or_404(Music, pk=pk)
    error=None
    user=request.user
    id=None
    message=None
    
    if user.is_staff or user == music.artist:   
        if request.method=='POST':
            form = MusicForm(request.POST, request.FILES, instance=music)
            if form.is_valid():
                try:  
                    music = form.save()         
                    # post=post.update(post=form.cleaned_data['post'], status=form.cleaned_data['status'])
                    id=music.id
                    message="Music Update successful"
                except:
                    error="There was a problem with your submission"
            else:
                error = "Your data is not complete"
        else:
            form= MusicForm(instance=music)
    
    context={
        'user':user,
        'music':music,
        'form':form,
        'id': id,
        'error': error,
        'message':message,
        }
    return render(request, template_name, context=context)

@login_required
def delete_music(request, pk, **kwargs):
    template_name='mike_admin/music/confirm_delete.html'
    final_template='mike_admin/music/delete_music.html'
    post= get_object_or_404(Music, pk=pk)
    error=None
    user=request.user
    id=None
    message= None
    
    if user.is_staff or user==post.artist:   
        if request.method=='POST':                          
            post=post.delete()
            message="The music has been successfully deleted"                   
            return render(request, final_template, {'post': post})    
                    
        else:
            
            form= MusicForm(instance=post)
    else:
        error="Your are not authorize to delete this music"
    
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
def music_detail(request, pk, **kwargs):
    template_name = 'mike_admin/music/music_detail.html'
    post = None    # Comment posted
    if request.method == 'POST' and request.user.is_staff:
        skiza_code = request.POST.get('skiza')
        post = Music.objects.filter(pk=pk)
        post.update(is_sent=True, skiza_code=skiza_code)
        post=get_object_or_404(Music, pk=pk)
    else:
        if request.user.is_staff:
            post = get_object_or_404(Music, pk=pk) 
        else:
            post = get_object_or_404(Music, pk=pk, artist=request.user) 
    context = {
        'post': post
    }
    return render(request, template_name, context=context)

# The Users controllers
class UserList(generic.ListView, LoginRequiredMixin, UserPassesTestMixin):
    queryset = get_user_model().objects.all().order_by('-date_joined')
    template_name = 'mike_admin/users/users.html'
    context_object_name= "accounts"
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

@login_required
@user_passes_test(lambda user: user.is_staff)
def user_detail(request, username, **kwargs):
    template_name = 'mike_admin/users/user_details.html'
    account = None    # Comment posted
    if request.user.is_staff:
            account = get_object_or_404(get_user_model(), username=username) 
    context = {
        'account': account
    }
    return render(request, template_name, context=context)

# The Transactions controllers
class LipaTransactionList(generic.ListView, LoginRequiredMixin, UserPassesTestMixin):
    """A class based view for showing all the transactions to the logged in user"""
    queryset = Lipa_na_mpesa.objects.all().order_by('-TransationDate')
    template_name = 'mike_admin/transactions/transactions.html'
    context_object_name= "lipa_transactions"
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff    
     
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the the successful and failed transactions
        context['lipa_successful'] = Initiate.objects.filter(ResultCode=1).order_by('-date_added')
        context['lipa_unsuccessful'] = Initiate.objects.filter(ResultCode=0).order_by('-date_added')
        return context
    

# The Transactions controllers
class C2BTransactionList(generic.ListView, LoginRequiredMixin, UserPassesTestMixin):
    queryset = C2BPaymentModel.objects.all().order_by('-TransTime')
    template_name = 'mike_admin/transactions/users.html'
    context_object_name= "cust_transactions"
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

# sendemail
from django.core.mail import send_mail

def sendemail(request):
    """this is a test email sender"""
    send_mail(
        'Subject here',
        'Here is the message.',
        'from@example.com',
        ['jets.starplus@gmail.com'],
        fail_silently=False,
    )
    return HttpResponse("success")

