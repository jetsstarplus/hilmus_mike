from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Post, Comment
from .forms import CommentForm, PostForm
from django.urls import reverse_lazy


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'article/index.html'
    paginate_by=10

def create_post(request):
    template_name='article/create_post.html'
    new_post=None
    error=None
    user=request.user
    
    if user.is_staff:   
        if request.method=='POST':
            form = PostForm(data=request.POST)
            if form.is_valid():
                new_post= form.save(commit=False)
                new_post.author= request.user
                new_post.save()
            else:
                error="There was a problem with your submission"
        else:
            form= PostForm()
    
    context={
        'user':user,
        'new_post':new_post,
        'form':form
        }
    return render(request, template_name, context=context)

 
def update_post(request, slug):
    template_name='article/create_post.html'
    post = get_object_or_404(Post, slug=slug)
    error=None
    user=request.user
    
    if user.is_staff:   
        if request.method=='POST':
            form = PostForm(data=request.POST)
            if form.is_valid():
                post= form.update()
            else:
                error="There was a problem with your submission"
        else:
            form= PostForm()
    
    context={
        'user':user,
        'post':post,
        'form':form
        }
    return render(request, template_name, context=context)

 

class PostUpdate(UpdateView):
    model= Post
    
    context_object_name='post'

class PostDelete(DeleteView):
    model= Post
    success_url= reverse_lazy('post')
    
def post_detail(request, slug):
    template_name = 'article/post_detail.html'
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
        'comment_form': comment_form
    }
    return render(request, template_name, context=context)
"""This post detail view will show the post and all its comments, let’s break it down to see what’s happening.

First, we assigned the HTML """

# Create your views here.
