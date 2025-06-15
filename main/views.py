from django.shortcuts import redirect, render, get_object_or_404
from django.http import FileResponse
import os
from django.conf import settings
from django.urls import reverse

from main.forms import BlogForm

from .models import BlogPost, Comment, Like
from django.views.decorators.csrf import csrf_exempt



def get_client_ip(request):
    """Get IP address of client"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def index(request):
    return render(request, 'main/index.html')

def about(request):
    return render(request, 'main/about.html')

def view_cv(request):
    file_path = os.path.join(settings.STATICFILES_DIRS[0], 'files', 'GCV-june.pdf')
    return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

def blog_list(request):
    posts = BlogPost.objects.all().order_by('-created_at')
    return render(request, 'main/blog_list.html', {'posts': posts})

@csrf_exempt
def blog_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    more_post = BlogPost.objects.exclude(slug=slug)

    # Handle new comment
    if request.method == 'POST' and 'comment_submit' in request.POST:
        name = request.POST.get('name')
        text = request.POST.get('text')
        if name and text:
            Comment.objects.create(post=post, name=name, text=text)

    # Handle like (based on IP address)
    if request.method == 'POST' and 'like_submit' in request.POST:
        ip = get_client_ip(request)
        if not Like.objects.filter(post=post, ip_address=ip).exists():
            Like.objects.create(post=post, ip_address=ip)

    comments = post.comments.all().order_by('-created_at')
    total_likes = post.total_likes()

    context = {
        'post': post,
        'more_post': more_post,
        'comments': comments,
        'total_likes': total_likes,
        'page': 'blog',
    }
    return render(request, 'main/blog_detail.html', context)

def blog_add(request):
    if request.method == 'POST':
        print("POST request received")
        print("Files in request:", request.FILES)
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            print("Form is valid")
            from django.core.files.storage import default_storage
            print("Current storage backend:", default_storage.__class__.__name__)
            blog_post = form.save()
            print("Image URL:", blog_post.image.url)
            return redirect(reverse('blog_list'))
        else:
            print("Form errors:", form.errors)
    else:
        form = BlogForm()
    context = {'form': form}
    return render(request, 'main/blog_add.html', context=context)
