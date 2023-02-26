from django.shortcuts import render
from django.urls import reverse
from .forms import PostForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def add_post(request):
    if request.method == 'POST':
        form = PostForm(data = request.POST, files = request.FILES)
        if form.is_valid():
            f = form.save(commit = False)
            f.author = request.user
            f.save()
        #else:
        return HttpResponseRedirect(reverse('account:user_profile', kwargs = {'id': request.user.id}))     # GET request to user_profil view   /// you can use reverse(request.user.get_absolute_url())
            






@login_required
def post_detail(request):
    pass