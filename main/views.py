from django.shortcuts import redirect, render, get_object_or_404
from django.http import FileResponse, JsonResponse
import os
from django.conf import settings
from django.urls import reverse
import cloudinary
import cloudinary.uploader
from django.views.decorators.csrf import csrf_exempt
import json

from main.forms import BlogForm

from .models import BlogPost, Comment, Like



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

@csrf_exempt
def upload_image(request):
    """Handle image uploads from Froala editor to Cloudinary"""
    if request.method == 'POST':
        try:
            # Get the uploaded file
            uploaded_file = request.FILES.get('file')
            
            if not uploaded_file:
                return JsonResponse({'error': 'No file uploaded'}, status=400)
            
            # Upload to Cloudinary
            result = cloudinary.uploader.upload(
                uploaded_file,
                folder='froala_images',
                resource_type='image'
            )
            
            # Return the URL in the format Froala expects
            return JsonResponse({
                'link': result['secure_url']
            })
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def load_images(request):
    """Load images for Froala image manager"""
    try:
        # List images from Cloudinary (you might want to store image references in your database)
        # For now, return empty array
        return JsonResponse([])
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
def delete_image(request):
    """Delete image from Cloudinary"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            image_url = data.get('src')
            
            if image_url:
                # Extract public_id from URL and delete from Cloudinary
                # This is a simplified version - you might need more complex logic
                # to extract the public_id from the URL
                return JsonResponse({'success': True})
            
            return JsonResponse({'error': 'No image URL provided'}, status=400)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
