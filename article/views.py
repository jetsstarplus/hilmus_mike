from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

from .models import Post, Comment
from .forms import CommentForm, PostForm, PostUpdateForm
from django.urls import reverse_lazy, reverse


class PostList(generic.ListView, LoginRequiredMixin):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'article/index.html'
    paginate_by=10

@login_required
def create_post(request):
    template_name='mike_admin/admin_forms/create.html'
    new_post=None
    error=None
    slug=None
    user=request.user
    message=None
    callbackurl=reverse('article:create_post')
    name='Post'
    breadcrum={
        'url': reverse('article:post'),
        'name':'Posts'
    }
    
    if user.is_staff:   
        if request.method=='POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():               
                new_post= form.save(commit=False)
                new_post.author= request.user
                new_post.save()
                print('passed')
                slug=new_post.slug
                print("last")
                message="Article Successfully Created"
                data={
                    'message':message,
                    'status':200,
                }
            else:
                error="There was a problem with your submission"
                data={
                    'message':error,
                    'status':400
                }
            return JsonResponse(data)
        else:
            form= PostForm()
    
    context={
        'user':user,
        'new_post':new_post,
        'form':form,
        'slug':slug,      
        'url':callbackurl,
        'breadcrum':breadcrum,
        'name':name
        }
    return render(request, template_name, context=context)

 
@login_required
def update_post(request, slug):
    template_name='mike_admin/admin_forms/edit.html'
    post = get_object_or_404(Post, slug=slug)
    error=None
    user=request.user
    slug=None
    message=None
    
    callbackurl=reverse('article:update_post', args = (post.slug, ))
    name='Post'
    breadcrum={
        'url': reverse('article:post'),
        'name':'Posts'
    }
    create_url=reverse('article:create_post')
    delete_url=reverse('article:delete_post', args=(post.slug, ))
    
    if user.is_staff:   
        if request.is_ajax():
            if request.user == post.author:
                form = PostUpdateForm(request.POST, request.FILES, instance=post)
                if form.is_valid():
                    try:  
                        form.save()         
                        # post=post.update(post=form.cleaned_data['post'], status=form.cleaned_data['status'])
                        slug=post.slug
                        message="Post Update successful"
                        data={
                            'message':message,
                            'status':200
                        }
                    except:
                        error="There was a problem with your submission"
                        data={
                            'message':error,
                            'status':503,
                        }
                else:
                    error = "Your data is not complete"
                    data={
                            'message':error,
                            'status':503,
                        }
                return JsonResponse(data)
        else:
            form= PostUpdateForm(instance=post)
    
    context={
        'user':user,
        'post':post,
        'form':form,
        'slug': slug,
        'url':callbackurl,
        'breadcrum':breadcrum,
        'name':name,
        'create_url':create_url,
        'delete_url':delete_url,
        }
    return render(request, template_name, context=context)

@login_required
def delete_post(request, slug):
    template_name='mike_admin/admin_forms/delete.html'
    post= get_object_or_404(Post, slug=slug)
    error=None
    user=request.user
    slug=None
    message= None
    callbackurl=reverse('article:delete_post', args=(post.slug, ))
    name='Blog'
    breadcrum={
        'url': reverse('article:post'),
        'name':'Blogs' 
    } 
    if user.is_staff:   
        if request.method=='POST' and request.is_ajax():
            if request.user == post.author:                           
                    post=post.delete()
                    message="The post has been successfully deleted"  
                    data={
                        'message':message,
                        'status':200,
                    }                 
            else:
                error ="You are not authorized to edit this post"   
                data={
                    'message':error,
                    'status':400
                }
            return JsonResponse(data)    
                    
        else:
            
            form= PostForm(instance=post)
    
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
def post_detail(request, slug):
    """This post detail view will show the post and all its comments, let’s break it down to see what’s happening.

First, we assigned the HTML """
    template_name = 'article/post_detail.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    unpublished_comments= post.comments.filter(active=False)
    new_comment = None
      
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
    else:
        comment_form = CommentForm()

    context = {
        'post': post,
        'comments':comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'unpublished_comments': unpublished_comments,
    }
    return render(request, template_name, context=context)

def publish_comment(request):
    if request.is_ajax() and request.user.is_staff and request.method=='POST':
        id = request.POST.get('id')
        action=request.POST.get('action')       
        comment = Comment.objects.filter(pk=id)
        if action=='publish':
            # print(action)
            # updating the comment
            comment.update(active=True)
            data={
                'status':200,
                'message':'published'
            }
        elif action=='delete':
            # print(action)
            # deleting the comment
            comment.delete()
            data={
                'status':200,
                'message':'Deleted'
            }
        return JsonResponse(data)
        

# Create your views here.
