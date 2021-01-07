from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Q
from django.http import JsonResponse
from django.core.mail import EmailMessage
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie

from article.models import Post, Comment
from mike_admin.models import Testimonial, StaffMember, TermsOfService, Service
from article.forms import CommentForm
from .models import Contact


# Create your views here.
def index(request):
    template_name='pages/index.html'
    testimonials = Testimonial.objects.filter(is_published=True).order_by('-date_added')[:10]
    teams= StaffMember.objects.filter(is_published=True).order_by('-rank')[:4]
    terms= TermsOfService.objects.all().order_by('-date_added')[:1]
    service_list=Service.objects.all().order_by('title')[:6]
    context={
        'testimonials': testimonials,
        'teams':teams,
        'terms':terms,
        'service_list': service_list,
        }
    return render(request, template_name, context=context)

# The contact page controler
def contact(request):
    template_name='pages/contact.html'
    return render(request, template_name, context={})

def shop(request):
    template_name='pages/coming.html'
    return render(request, template_name, context={})

# Create your views here.
def terms(request):
    template_name='pages/terms.html'    
    post_list = Post.objects.filter(status=1).order_by('-created_on')
    terms= TermsOfService.objects.all().order_by('-date_added')[:1]    
    service_list=Service.objects.all().order_by('title')[:6]
    context={
        'terms':terms,
        'post_list':post_list,
        'service_list':service_list
        }
    return render(request, template_name, context=context)


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'pages/blog.html'
    # context_object_name="post_list"
    paginate_by=10
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['service_list'] = Service.objects.all().order_by('-title')[:6]
        return context
    # def get_queryset(self): # new
    #     return(Posts.objects.filter(
    #         Q(name__icontains='Boston') | Q(state__icontains='NY')
    #     ), Post.objects.filter(status=1).order_by('-created_on'))
    
    

class PostSearchList(generic.ListView):
    template_name = 'pages/search.html'    
    paginate_by=10
    def get_queryset(self): # new
        query = self.request.GET.get('q')
        return Posts.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)).order_by('-created_on')
        
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['service_list'] = Service.objects.all().order_by('title')[:6]
        return context


def post_detail(request, slug):
    template_name = 'pages/blog-details.html'
    post_list=Post.objects.filter(status=1).order_by('-created_on')[: 5]
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)       
    service_list=Service.objects.all().order_by('title')[:6]
    new_comment = None
    # Comment posted
    if request.is_ajax():
        email = request.POST.get("email", None)
        name = request.POST.get("name", None)
        body = request.POST.get("body", None)
        try:
            comment=Comment(name=name, email=email, body=body, post=post)           
            comment.save()
            data = {
                'message': "Your Comment is Awaiting Moderation, Thank you !",
                'status':200                
            }
        except:
            data = {
                'message': "There Was an Error in Your Reply !",
                'status':500                
            }
        finally:            
            return JsonResponse(data)
        # comment_form = CommentForm(data=request.POST)
        # if comment_form.is_valid():

        #     # Create Comment object but don't save to database yet
        #     new_comment = comment_form.save(commit=False)
        #     # Assign the current post to the comment
        #     new_comment.post = post
        #     # Save the comment to the database
        #     new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'post_list': post_list,
        'service_list':service_list,
    }
    return render(request, template_name, context=context)


def service(request, slug):
    template_name = 'pages/services.html'
    services=Service.objects.all()
    service = get_object_or_404(Service, slug=slug)    
    service_list=Service.objects.all().order_by('title')[:6]
    
    context = {
        'service': service,
        'services': services,
        'service_list':service_list,
    }
    return render(request, template_name, context=context)


#This is the form submission view
# @ensure_csrf_cookie(submit_contacts())
def submit_contacts(request):
    if request.is_ajax():
        email = request.POST.get("email", None)
        name = request.POST.get("name", None)
        subject = request.POST.get("subject", None)
        message = request.POST.get("message", None)
        # print(message)
                    
        try:
            contact = Contact.objects.create(email=email, full_name = name, subject=subject, content=message)
            final="Sender: {}\n Email: {}\n Message: \n {}".format(name,email, message)
            mail = EmailMessage(
                subject=subject, body=final, 
                from_email= 'Website Contact <{}>'.format(settings.DEFAULT_FROM_EMAIL),
                headers={'Message-ID': 'MIKE Creatives'},
                to=['connect@mikecreatives.com','jets.starplus@gmail.com', 'hilmus.software@gmail.com', 'w.mwangi95@gmail.com', 'mikecreatives254@gmail.com'])
            contact.save()
            # mail.content_subtype = ''
            mail.send()
            data = {
                'message': "Your Message has been Sent, Thank You!",
                'status':200
                
            }
            # print("This is executed as ok")
            
        except:
            data = {
                'message': "There was an error in your submission!",
                'status':500
            }
            # print("this is executed")
        
        finally:              
            return JsonResponse(data)
        
#this is the subscription form submission

def submit_subscription(request):
    if request.is_ajax():
        email = request.POST.get("email", None)
        
        try:
            subscribe = Subscribers.objects.create(email=email)
            subscribe.save()
            data  = {
                'messge':"OK"
            }
            
        except:
            data = {
                'messge':"You're already subscribed, Thank You"
            }
            
            
        finally:              
            return JsonResponse(data)

       
