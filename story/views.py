from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import StoryForm
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

@login_required
def add_story(request):
    if request.method == 'POST':
        form = StoryForm(data = request.POST, files = request.FILES)
        if form.is_valid():
            f = form.save(commit = False)
            f.owner = request.user
            f.save()
            
            return HttpResponseRedirect(reverse('account:user_profile', kwargs = {'id': request.user.id}))
    # else:
        # return render(request, 'story/story_form.html', {'storyform': StoryForm()})


