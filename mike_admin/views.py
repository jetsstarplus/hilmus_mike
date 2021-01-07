from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView, TemplateView, RedirectView
from django.conf import settings
from django.urls import reverse, reverse_lazy
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from datetime import datetime, timedelta
from django.utils import timezone
from django.views import generic
from django.contrib import messages
from django.http import HttpResponse, JsonResponse

from .models import Music, Testimonial, StaffMember, TermsOfService, Service
from article.models import Post, Comment
from daraja.models import Lipa_na_mpesa, C2BPaymentModel, Initiate

from .forms import ProfileForm, TestimonialForm, TermsForm, StaffMemberForm, MusicForm, ServiceForm

@login_required
def home(request): 
    user_music=Music.objects.filter(artist=request.user).order_by('-date_added')
    users=None
    musics=None
    testimonials=None
    new_users=0
    user_percentage=0
    lipa_transactions=None
    paybill=None
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
        paybill=C2BPaymentModel.objects.all().order_by('-TransTime')
    
    elif request.user:        
        if request.user.first_name==None or request.user.last_name==None or request.user.avatar==None:             
            messages.add_message(request, messages.WARNING,  "Please Ensure You Complete Your Profile")
            
            if request.user.is_payed==False:            
                messages.add_message(request, messages.INFO,  "Please Complete Your Payment First Inorder To Proceed")  
                
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
        'paybill':paybill
    }
    return render(request, template_name='mike_admin/dashboard-2.html', context=context )

@login_required
def profile(request):
    profile=None    
    comments=None
    new_comments=None
    if request.user.is_authenticated:
        profile = get_object_or_404(get_user_model(), pk=request.user.pk)
        musics = Music.objects.filter(artist=request.user.pk).all()
        boomplay= Music.objects.filter(artist=request.user.pk, is_boompay=True).count()
        music_number= musics.count()
        articles = Post.objects.filter(author=request.user.pk, status=1)
        skiza=Music.objects.filter(artist=request.user.pk, is_skiza=True).count()
        transactions=Initiate.objects.filter(ResultCode=0, user=request.user)  
        items=Comment.objects.filter(active=False)    
        comments=items.count()
        new_comments=items.order_by('-created_on')
                
    else:
        profile=None
    context={
        'profile': profile, 
        'musics': musics, 
        'music_number':music_number,
        'boomplay':boomplay,
        'article':articles,
        'skiza': skiza,
        'transactions':transactions,        
        'comments':comments,
        'new_comments':new_comments,
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
    queryset = Testimonial.objects.all().order_by('-date_added')
    template_name = 'mike_admin/testimonials/index.html'
    context_object_name='testimonials'
    paginate_by=10
    
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    

@login_required
@user_passes_test(lambda user: user.is_staff)
def create_testimonial(request):
    template_name='mike_admin/admin_forms/create.html'
    new_post=None
    error=None
    user=request.user
    message=None
    callbackurl=reverse('mike_admin:create_testimonial')
    name='Testimonial'
    breadcrum={
        'url': reverse('mike_admin:testimonials'),
        'name':'Testimonials'
    }
    
    if user.is_staff:   
        if request.is_ajax() and request.method=='POST':
            form = TestimonialForm(request.POST, request.FILES)
            if form.is_valid():
                # id=2
                # pass
                new_post= form.save(commit=False)
                new_post.added_by= request.user
                message=" Testimonial Successfully Created!"
                new_post.save()
                id=new_post.id
                data={
                    'message':message,
                    'status':200,
                    'id':id
                }
            else:
                error="There was a problem with your submission"
                data={
                    'message':error,
                    'status':400
                }
            return JsonResponse(data)
        else:
            form= TestimonialForm()
    
    context={
        'user':user,
        'new_post':new_post,
        'form':form,
        'url':callbackurl,
        'breadcrum':breadcrum,
        'name':name
        }
    return render(request, template_name, context=context)

@login_required
@user_passes_test(lambda user: user.is_staff)
def update_testimonial(request, id):
    template_name='mike_admin/admin_forms/edit.html'
    post = get_object_or_404(Testimonial, pk=id)
    error=None
    user=request.user
    message=None
    callbackurl=reverse('mike_admin:update_testimonial', args = (post.id, ))
    name='Testimonial'
    breadcrum={
        'url': reverse('mike_admin:testimonials'),
        'name':'Testimonials'
    }
    create_url=reverse('mike_admin:create_testimonial')
    delete_url=reverse('mike_admin:delete_testimonial', args=(post.id, ))
    
    
    if user.is_staff:   
        if request.is_ajax() and request.method=='POST':
            form = TestimonialForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                try:  
                    form.save()         
                    # post=post.update(post=form.cleaned_data['post'], status=form.cleaned_data['status'])
                    id=post.id
                    message="Testimonial Update successful!"
                    data={
                        'message':message,
                        'status':200
                    }
                except:
                    error="There was a problem with your submission!"
                    data={
                        'message':error,
                        'status':503
                    }
            else:
                error = "Your data is not complete!"
                data={
                        'message':error,
                        'status':400
                    }
            return JsonResponse(data)
        else:
            form= TestimonialForm(instance=post)
    
    context={
        'user':user,
        'post':post,
        'form':form,
        'url':callbackurl,
        'breadcrum':breadcrum,
        'name':name,
        'create_url':create_url,
        'delete_url':delete_url,
        }
    return render(request, template_name, context=context)

@login_required
@user_passes_test(lambda user: user.is_staff)
def delete_testimonial(request, id):
    template_name='mike_admin/admin_forms/delete.html'
    post= get_object_or_404(Testimonial, id=id)
    user=request.user
    message= None
    
    callbackurl=reverse('mike_admin:delete_testimonial', args=(post.id, ))
    name='Testimonial'
    breadcrum={
        'url': reverse('mike_admin:testimonials'),
        'name':'Testimonial' 
    } 
    
    if user.is_staff:   
        if request.method=='POST' and request.is_ajax():                         
            post=post.delete()
            message="The testimonial has been successfully deleted"                   
            data={
                'message':message,
                'status':200   
            }
            return JsonResponse(data)  
                    
        else:            
            form= TestimonialForm(instance=post)
    else:
        error ="You are not authorized to edit this post"   
             
    context={
        'user':user,
        'post':post,
        'form':form,      
        'name':name,
        'breadcrum':breadcrum,
        'url':callbackurl
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
    queryset = StaffMember.objects.all().order_by('-rank')
    template_name = 'mike_admin/staff/index.html'
    context_object_name='staffs'
    paginate_by=10
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

@login_required
@user_passes_test(lambda user: user.is_staff)
def create_staff(request):
    template_name='mike_admin/admin_forms/create.html'
    new_post=None
    error=None
    user=request.user
    message= None
    callbackurl=reverse('mike_admin:create_staff')
    name='Staff Member'
    breadcrum={
        'url': reverse('mike_admin:staffs'),
        'name':'Staff'
    }
    
    if user.is_staff:   
        if request.method=='POST' and request.is_ajax():
            form = StaffMemberForm(request.POST, request.FILES)
            if form.is_valid():
               new_post =form.save()
               id= new_post.id               
               message=" Staff Member Successfully created!"
               data={
                   'message':message,
                   'status':200
               }
            else:
                error="There was a problem with your submission"
                data={
                    'message':error,
                    'status':400
                }
            return JsonResponse(data)
        else:
            form= StaffMemberForm()
    
    context={
        'user':user,
        'new_post':new_post,
        'form':form,
        'url':callbackurl,
        'breadcrum':breadcrum,
        'name':name
        }
    return render(request, template_name, context=context)

@login_required
@user_passes_test(lambda user: user.is_staff)
def update_staff(request, id):
    template_name='mike_admin/admin_forms/edit.html'
    post = get_object_or_404(StaffMember, pk=id)
    error=None
    user=request.user
    message=None
    
    callbackurl=reverse('mike_admin:update_staff', args = (post.id, ))
    name='Staff Member'
    breadcrum={
        'url': reverse('mike_admin:staffs'),
        'name':'Staff'
    }
    create_url=reverse('mike_admin:create_staff')
    delete_url=reverse('mike_admin:delete_staff', args=(post.id, ))
    
    
    if user.is_staff:   
        if request.method=='POST' and request.is_ajax():
            form = StaffMemberForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                try:  
                    form.save()         
                    # post=post.update(post=form.cleaned_data['post'], status=form.cleaned_data['status'])
                    id=post.id
                    message="Staff Information Updated successful"
                    data={
                        'message':message,
                        'status':200
                    }
                except:
                    error="There was a problem with your submission"
                    data={
                        'message':error,
                        'status':400
                    }
            else:
                error = "Your data is not complete"
                data={
                    'message':error,
                    'status':500
                }
            return JsonResponse(data)
        else:
            form= StaffMemberForm(instance=post)
    
    context={
        'user':user,
        'post':post,
        'form':form,
        'url':callbackurl,
        'breadcrum':breadcrum,
        'name':name,
        'create_url':create_url,
        'delete_url':delete_url,
        }
    return render(request, template_name, context=context)

@login_required
@user_passes_test(lambda user: user.is_staff)
def delete_staff(request, id):
    template_name='mike_admin/admin_forms/delete.html'
    post= get_object_or_404(StaffMember, id=id)
    error=None
    user=request.user
    id=None
    message= None
     
    callbackurl=reverse('mike_admin:delete_staff', args=(post.id, ))
    name='Staff Member'
    breadcrum={
        'url': reverse('mike_admin:staffs'),
        'name':'Staff' 
    } 
    
    if user.is_staff:   
        if request.method=='POST' and request.is_ajax():
            if request.user:                           
                    post=post.delete()
                    message="The staff member has been successfully deleted"  
                    data={
                        'message':message,
                        'status':200
                    }                
            else:
                error ="You are not authorized to edit this staff" 
                data={
                    'message':error,
                    'status':400
                }  
                
            return JsonResponse(data)   
                    
        else:
            
            form= StaffMemberForm(instance=post)
            
    else:
        error ="You are not authorized to edit this staff"     
    context={
        'user':user,
        'post':post,
        'form':form,      
        'name':name,
        'breadcrum':breadcrum,
        'url':callbackurl
        }
    return render(request, template_name, context=context)
    
@login_required
@user_passes_test(lambda user: user.is_staff)
def staff_detail(request, id):
    template_name = 'mike_admin/staff/staff_detail.html'
    post = get_object_or_404(StaffMember, pk=id)     # Comment posted
    
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
    template_name='mike_admin/admin_forms/create.html'
    new_post=None
    error=None
    user=request.user
    message=None
    callbackurl=reverse('mike_admin:create_terms')
    name='Term Of Service'
    breadcrum={
        'url': reverse('mike_admin:terms'),
        'name':'Terms Of Service'
    }
    
    
    if user.is_staff:   
        if request.method=='POST' and request.is_ajax():
            form = TermsForm(request.POST, request.FILES)
            if form.is_valid():
               new_post= form.save()
               message=" Terms Of Service Successfully created!"
               data={
                   'message':message,
                   'status':200
               }
            else:
                error="There was a problem with your submission"
                data={
                    'message':error,
                    'status':400
                }
            return JsonResponse(data)
        else:
            form= TermsForm()
    
    context={
        'user':user,
        'new_post':new_post,
        'form':form,
        'url':callbackurl,
        'breadcrum':breadcrum,
        'name':name
        }
    return render(request, template_name, context=context)

@login_required
@user_passes_test(lambda user: user.is_staff)
def update_terms(request, id):
    template_name='mike_admin/admin_forms/edit.html'
    terms = get_object_or_404(TermsOfService, pk=id)
    error=None
    user=request.user
    message=None
    callbackurl=reverse('mike_admin:update_terms', args = (terms.id, ))
    name='Terms Of Service'
    breadcrum={
        'url': reverse('mike_admin:terms'),
        'name':'Terms Of Service'
    }
    create_url=reverse('mike_admin:create_terms')
    delete_url=reverse('mike_admin:delete_terms', args=(terms.id, ))
    
    if user.is_staff:   
        if request.method=='POST' and request.is_ajax():
            form = TermsForm(request.POST, request.FILES, instance=terms)
            if form.is_valid():
                try:  
                    terms = form.save()         
                    # post=post.update(post=form.cleaned_data['post'], status=form.cleaned_data['status'])
                    id=terms.id
                    message="Terms Update successful"
                    data={
                        'message':message,
                        'status':200
                    }
                except:
                    error="There was a problem with your submission"
                    data={
                        'message':error,
                        'status':400
                    }
            else:
                error = "Your data is not complete"
                data={
                            'message':error,
                            'status':400
                        } 
            return JsonResponse(data)
               
        else:
            form= TermsForm(instance=terms)
    
    context={
        'user':user,
        'terms':terms,
        'form':form,
        'url':callbackurl,
        'breadcrum':breadcrum,
        'name':name,
        'create_url':create_url,
        'delete_url':delete_url,
        }
    return render(request, template_name, context=context)

@login_required
@user_passes_test(lambda user: user.is_staff)
def delete_terms(request, id):
    template_name='mike_admin/admin_forms/delete.html'
    post= get_object_or_404(TermsOfService, id=id)
    error=None
    user=request.user
    id=None
    message= None  
    callbackurl=reverse('mike_admin:delete_terms', args=(post.id, ))
    name='Terms Of Service'
    breadcrum={
        'url': reverse('mike_admin:terms'),
        'name':'Terms Of Service' 
    } 
    
    if user.is_staff:   
        if request.method=='POST' and request.is_ajax():
            if request.user:                           
                    post=post.delete()
                    message="The term of service has been successfully deleted" 
                    data={
                    'message':message,
                    'status':200
                     }                   
            else:
                error ="You are not authorized to edit this page"                 
                data={
                    'message':error,
                    'status':200
                } 
            return JsonResponse(data)      
                    
        else:
            
            form= TermsForm(instance=post)
    
    context={
        'user':user,
        'post':post,
        'form':form,        
        'name':name,
        'breadcrum':breadcrum,
        'url':callbackurl
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
    template_name='mike_admin/admin_forms/create.html'
    new_post=None
    error=None
    user=request.user
    form=None
    message=None
    callbackurl=reverse('mike_admin:create_music')
    name='Music'
    breadcrum={
        'url': reverse('mike_admin:music'),
        'name':'Musics'
    }
    
    if user.is_payed or user.is_staff:   
        if request.method=='POST' and request.is_ajax():           
            form = MusicForm(request.POST, request.FILES)
            if form.is_valid():
               new_post= form.save(commit=False)
               new_post.artist= user
               new_post.save()
               message="Your Music Has Been Successfully Uploaded!"
               data={
                   'message':message,
                   'status':200
               }
            else:
                error="There was a problem with your submission"
                data={
                    'message':error,
                    'status':400
                }
            return JsonResponse(data)
        else:
            form= MusicForm()
    else:
        error="Please Complete the payment first"
    
    context={
        'user':user,
        'new_post':new_post,
        'form':form,        
        'url':callbackurl,
        'breadcrum':breadcrum,
        'name':name
        }
    return render(request, template_name, context=context)

@login_required
def update_music(request, pk, **kwargs):
    template_name='mike_admin/admin_forms/edit.html'
    music = get_object_or_404(Music, pk=pk)
    error=None
    user=request.user
    message=None
    callbackurl=reverse('mike_admin:update_music', args = (music.id, ))
    name='Music'
    breadcrum={
        'url': reverse('mike_admin:music'),
        'name':'Musics'
    }
    create_url=reverse('mike_admin:create_music')
    delete_url=reverse('mike_admin:delete_music', args=(music.id, ))
    
    if user.is_staff or user == music.artist:   
        if request.method=='POST' and request.is_ajax():
            form = MusicForm(request.POST, request.FILES, instance=music)
            if form.is_valid():
                try:  
                    music = form.save()         
                    # post=post.update(post=form.cleaned_data['post'], status=form.cleaned_data['status'])                    
                    message="Music Updated successfully!"
                    data={
                        'message':message,
                        'status':200
                    }
                except:
                    error="There was a problem with your submission!"
                    data={
                        'message':error,
                        'status':400
                    }
            else:
                error = "Your data is not complete!"
                data={
                        'message':error,
                        'status':400
                    }
            return JsonResponse(data)
        else:
            form= MusicForm(instance=music)
    
    context={
        'user':user,
        'music':music,
        'form':form,
        'url':callbackurl,
        'breadcrum':breadcrum,
        'name':name,
        'create_url':create_url,
        'delete_url':delete_url,
        }
    return render(request, template_name, context=context)

@login_required
def delete_music(request, pk, **kwargs):
    template_name='mike_admin/admin_forms/delete.html'
    post= get_object_or_404(Music, pk=pk)
    error=None
    user=request.user
    message= None
    callbackurl=reverse('mike_admin:delete_music', args=(post.id, ))
    name='Music'
    breadcrum={
        'url': reverse('mike_admin:music'),
        'name':'Musics'
    }
    
    if user.is_staff or user==post.artist:   
        if request.method=='POST' and request.is_ajax():                          
            post=post.delete()
            message="The music has been successfully deleted!"  
            data={
                'message':message,
                'status':200
            } 
            return JsonResponse(data)                
                  
        else:
            
            form= MusicForm(instance=post)
    else:
        error="Your are not authorized to delete this music!"
        data={
                'message':error,
                'status':200
            } 
        return JsonResponse(data)
    
    context={
        'user':user,
        'post':post,
        'form':form,
        'name':name,
        'breadcrum':breadcrum,
        'url':callbackurl
        }
    return render(request, template_name, context=context)
    
@login_required
def music_detail(request, pk, **kwargs):
    template_name = 'mike_admin/music/music_detail.html'
    post = None    # Comment posted
    if request.method == 'POST' and request.user.is_staff and request.is_ajax():
        skiza_code = request.POST.get('skiza')
        post = Music.objects.filter(pk=pk)
        post.update(is_sent=True, skiza_code=skiza_code)
        post=get_object_or_404(Music, pk=pk)
        data={
            'message':'Successfully Published',
            'status':200
        }
        return JsonResponse(data)
    else:
        if request.user.is_staff:
            post = get_object_or_404(Music, pk=pk) 
        else:
            post = get_object_or_404(Music, pk=pk, artist=request.user) 
    context = {
        'post': post
    }
    return render(request, template_name, context=context)

# The services controllers
class ServicesList(generic.ListView, LoginRequiredMixin, UserPassesTestMixin):
    queryset = Service.objects.all().order_by('-date_added')
    template_name = 'mike_admin/services/index.html'
    context_object_name= "services"
    paginate_by=10
    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff

@login_required
@user_passes_test(lambda user: user.is_staff)
def create_service(request):
    template_name='mike_admin/admin_forms/create.html'
    service=None
    error=None
    user=request.user
    message=None
    callbackurl=reverse('mike_admin:create_service')
    name='Service'
    breadcrum={
        'url': reverse('mike_admin:services'),
        'name':'Services'
    }
    
    
    if user.is_staff:   
        if request.method=='POST' and request.is_ajax():
            form = ServiceForm(request.POST, request.FILES)
            if form.is_valid():
               service = form.save()
               message=" Service Successfully created!"
               data={
                   'message':message,
                   'status':200
               }
            else:
                error="Your Information is Incomplete!"
                data={
                    'message':error,
                    'status':400
                }
            return JsonResponse(data)
        else:
            form= ServiceForm()
    
    context={
        'user':user,
        'form':form,
        'service':service,
        'url':callbackurl,
        'breadcrum':breadcrum,
        'name':name
        }
    return render(request, template_name, context=context)

@login_required
@user_passes_test(lambda user: user.is_staff)
def update_service(request, slug):
    template_name='mike_admin/admin_forms/edit.html'
    service = get_object_or_404(Service, slug=slug)
    error=None
    user=request.user
    message=None
    callbackurl=reverse('mike_admin:update_service', args = (service.id, ))
    name='Service'
    breadcrum={
        'url': reverse('mike_admin:services'),
        'name':'Services'
    }
    create_url=reverse('mike_admin:create_service')
    delete_url=reverse('mike_admin:delete_service', args=(service.id, ))
    
    if user.is_staff:   
        if request.method=='POST' and request.is_ajax():
            form = ServiceForm(request.POST, request.FILES, instance=service)
            if form.is_valid():
                try:  
                    form.save()         
                    # post=post.update(post=form.cleaned_data['post'], status=form.cleaned_data['status'])
                    
                    message="Service Update successful!"
                    data={
                        'message':message,
                        'status':200
                    }
                except:
                    error="There was a problem with your submission!"
                    data={
                        'message':error,
                        'status':400
                    }
            else:
                error = "Your data is not complete"
                data={
                            'message':error,
                            'status':400
                        } 
            return JsonResponse(data)
               
        else:
            form= ServiceForm(instance=service)
    
    context={
        'user':user,
        'form':form,
        'service':service,
        'url':callbackurl,
        'breadcrum':breadcrum,
        'name':name,
        'create_url':create_url,
        'delete_url':delete_url,
        }
    return render(request, template_name, context=context)

@login_required
@user_passes_test(lambda user: user.is_staff)
def delete_service(request, slug):
    template_name='mike_admin/admin_forms/delete.html'
    service= get_object_or_404(Service, slug=slug)
    error=None
    user=request.user
    message= None  
    callbackurl=reverse('mike_admin:delete_service', args=(service.slug, ))
    name='Service'
    breadcrum={
        'url': reverse('mike_admin:services'),
        'name':'Services' 
    } 
      
    if request.method=='POST' and request.is_ajax():
        if request.user.is_staff:                           
                service.delete()
                message="The term of service has been successfully deleted" 
                data={
                'message':message,
                'status':200
                    }                   
        else:
            error ="You are not authorized to edit this page"                 
            data={
                'message':error,
                'status':200
            } 
        return JsonResponse(data)      
         
    
    context={
        'user':user,
        'post':service,        
        'name':name,
        'breadcrum':breadcrum,
        'url':callbackurl
        }
    return render(request, template_name, context=context)
    
@login_required
def service_detail(request, slug):
    template_name = 'mike_admin/services/se_detail.html'
    service = get_object_or_404(Service, slug=slug)     # Comment posted
    
    context = {
        'service': service
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
    musics=None
    upload=None
    if request.user.is_staff:
            account = get_object_or_404(get_user_model(), username=username) 
            musics=Music.objects.filter(artist=account, is_sent=False)
            upload=Music.objects.filter(artist=account, is_sent=True)
    context = {
        'account': account,
        'musics':musics,
        'upload':upload
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
        context['lipa_successful'] = Initiate.objects.filter(ResultCode=0).order_by('-date_added')
        context['lipa_unsuccessful'] = Initiate.objects.filter(ResultCode=1).order_by('-date_added')
        context['paybill']=C2BPaymentModel.objects.filter(Status=True).order_by('-TransTime')
        context['paybill_unconfirmed']=C2BPaymentModel.objects.filter(Status=False).order_by('-TransTime')
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
    email=send_mail(
        'Subject here',
        'Here is the message.',
        'Test <{}>'.format(settings.DEFAULT_FROM_EMAIL),
        ['jets.starplus@gmail.com'],
        fail_silently=False,
    )
    if email:    
        return HttpResponse("success")
    else:
        return HttpResponse('Failed')
   
"""This method returns a response to the ajax-request.js with the relevant data""" 
def requestMessages(request):
    # initializing an empty list
    com=[]
    """This is an ajax request for displaying the uncommented on messages"""
    if request.is_ajax() and request.user.is_staff:
        if request.method=='POST':
            pass
        else:
            items=Comment.objects.filter(active=False)
            comments=items.count()
            new_comments=items.order_by('-created_on')
            for comment in new_comments:
                # Adding the comments to a dictionary inside a list
                com_dic=[{'id':comment.id},{'body':comment.body}, {'name':comment.name}, {'date': comment.created_on}]
                com.append(com_dic)                
                # print(com)
            data={
                'comments':comments,
                'new_comments':com,
            }
            return JsonResponse(data)
