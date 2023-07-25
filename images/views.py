from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ImageCeateForm
from django.shortcuts import get_object_or_404
from .models import Image
from django.http import JsonResponse
from django.views.decorators.http import require_POST

# Create your views here.
@login_required
def image_create(request):
    if request.method == "POST":
        form = ImageCeateForm(request.POST)
        
        if form.is_valid():
            cd = form.cleaned_data
            new_image = form.save(commit=False)
            
            new_image.user = request.user
            new_image.save()
            messages.success(request, 'Image added succesfully')
            
            return redirect(new_image.get_absolute_url())
    else:
        form = ImageCeateForm(data=request.GET)
            
    return render(request, 'images/image_create.html', {'form':form, 'section':'images'})


def image_detail(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image_detail.html', {'image':image})

@login_required
@require_POST
def image_like(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users_like.add(request.user)
            else:
                image.user_like.remove(request.user)
            return JsonResponse({"status": 'ok'})
        except Image.DoesNotExist:
            pass
    return JsonResponse({"status": 'error'})
