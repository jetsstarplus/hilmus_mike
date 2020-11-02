from django.shortcuts import render
from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Q
from django.http import JsonResponse

from article.models import Post
from article.forms import CommentForm
from .models import Contact


# Create your views here.
def index(request):
    template_name='pages/index.html'
    posts = Post.objects.filter(status=1).all().order_by('-created_on')[:3]
    context={'posts': posts}
    return render(request, template_name, context=context)


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'pages/blog.html'
    paginate_by=10
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


def post_detail(request, slug):
    template_name = 'pages/blog-details.html'
    post_list=Post.objects.filter(status=1).order_by('-created_on')[: 5]
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    # Comment posted
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():

            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'post_list': post_list
    }
    return render(request, template_name, context=context)

#This is the form submission view
def submit_contacts(request):
    if request.is_ajax():
        email = request.POST.get("email", None)
        name = request.POST.get("name", None)
        subject = request.POST.get("subject", None)
        message = request.POST.get("message", None)
        # print(message)
                    
        try:
            contact = Contact.objects.create(email=email, full_name = name, subject=subject, content=message)
            contact.save()
            data = {
                'message': "OK"
            }
            # print("This is executed as ok")
            
        except:
            data = {
                'message': "There was an error in our side"
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
