from django.utils import timezone
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template.loader import render_to_string
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import UserProf, Contact, Re_quest, Blocking, Direct
from story.models import StoryModel
from .forms import LoginForm, RegistrationForm, createuserform, changepassform, EditProfile
from posts.forms import PostForm
from story.forms import StoryForm


def users_list(request):
    return render(request, 'account/users_list.html', {'users': UserProf.objects.filter(is_active = True)})
    
   
@login_required(login_url = 'account:login', redirect_field_name = 'next')
def user_profile(request, id):
    obj = get_object_or_404(UserProf, id=id)
    
    if request.method == 'POST':
        from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

        def is_ajax(request):
            return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'
            
        posts = obj.posts.filter(showing = True).order_by('-created')
        paginator = Paginator(posts,8)  
        page = request.GET.get('page')      #you get value of page parameter using GET method, because   .../?page=5   is GET method
        

        try:
            posts = paginator.page(page)
            
        except PageNotAnInteger:
            # If page is not an integer deliver the first page
            posts = paginator.page(1)
            print('PageNotAnInteger')
        except EmptyPage:
            if is_ajax(request):
                # If the request is AJAX and the page is out of range
                # return an empty page 
                print('EmptyPage')
                return HttpResponse('')   # return data = ''
            # If page is out of range deliver last page of results
            posts = paginator.page(paginator.num_pages)
            print('paginator.page(paginator.num_pages)')
        if is_ajax(request):
            return render(request,  'account/list_ajax.html',  {'section': 'posts', 'posts': posts})     # every request to load more posts, this line is executed
            
        return HttpResponseRedirect(reverse('account:user_profile', kwargs = {'id': request.user.id}))
    
    # request.method is : GET    
    try :
        posts = obj.posts.filter(showing = True).order_by('-created')[:8] # last created story should be in last (Ascending order)  ### the first 6 elements will return
        if len(posts) == 0:
            posts = False
    except:
        posts = False
        
    now = timezone.now()
    last = now - timezone.timedelta(hours = 10) # other methods : seconds, minutes !
    try :
        stories = StoryModel.objects.filter(owner = obj, created__gte = last).order_by('created')  # last created story should be in last (Ascending order)
        if len(stories) == 0:
            stories = False
    except:
        stories = False
    
    return render(request, 'account/user_profile.html', {'obj': obj, 'posts': posts, 'stories': stories, 'storyform': StoryForm(), 'editprofileform': EditProfile(instance = request.user) \
                                                                        , 'addpostform': PostForm()}) 
    

@login_required
def Edit_Profile(request):
    if request.method == 'POST':
        form = EditProfile(instance = request.user, data = request.POST, files = request.FILES)
        #print(form.is_valid())
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('account:user_profile', kwargs = {'id': request.user.id}))
            
            

            
@login_required         
def my_directs_view(request):
    def dedupe(items):
        seen = set()
        add = seen.add
        for item in items:
            if item not in seen:
                yield item
                add(item)
    
    a = list(request.user.my_directs.values_list('id', flat = True) ) + list(request.user.directs_me.values_list('id', flat = True) )   # request.user.directs_me.values_list('id', flat = True) is  QuerySet, so we convert it to list, if we
                            # don't this we take an error : eperand (+) is not support by QuerySet !
    # print(a)                # [14, 14, 14, 14, 12, 12, 14, 14, 14, 14, 12]
    b = list(dedupe(a))
    # print(b)                # [14, 12]
    users = UserProf.objects.filter(id__in = b)
    # print(users)            # <QuerySet [<UserProf: nonoka>, <UserProf: without_img>]>                id of nonka user is 14, and 12 is for without_img user !
    if len(users) is 0 :
        users = False
    return render(request, 'account/directs_list.html', {'users': users})
    

@login_required
def direct(request, id):

    obj = get_object_or_404(UserProf, id=id)
    if request.method == 'POST':
        d1 = Direct.objects.create(user_from = request.user, user_to = obj, text = request.POST.get('msg'))
        return JsonResponse({'status': 'ok', 'time': d1.created.strftime("%d/%b/%Y - %R")})
    else: 
        from operator import attrgetter
        from itertools import chain
        
        q1 = Direct.objects.filter(user_from = request.user, user_to = obj, show = True)
        q2 = Direct.objects.filter(user_from = obj, user_to = request.user, show = True)
        # print()
        if len(q1) == 0 and len(q2) ==0 :
            results = False
        else:
            results = sorted(chain(q1, q2), key=attrgetter('created'))
        # print((q1|q2))
        return render(request, 'account/direct.html', {'obj': obj, 'results': results})
    
    
@login_required                                              
def follow_unfollow(request):
    if request.method=='POST':
        obj_id  = request.POST.get('id')
        action  = request.POST.get('action')
        
        if action and obj_id:
            try:
                obj  = UserProf.objects.get(id=obj_id)
                if action=='follow':
                    Contact.objects.create(user_from = request.user, user_to = obj)
                elif action=='unfollow' :
                    Contact.objects.get(user_from = request.user, user_to = obj).delete()
                    
                
                return JsonResponse({'status': 'ok', 'user_followers': obj.followers.count(), 'user_followings': obj.following.count()})
            except:
                pass
        return JsonResponse({'status': 'error'})
        

@login_required 
def follow_request_requested(request):
    if request.method=='POST':
        obj_id  = request.POST.get('id')
        action  = request.POST.get('action')
        
        if action and obj_id:
           
            try:
                obj  = UserProf.objects.get(id=obj_id)
                
                if action=='unfollow':
                    
                    Contact.objects.get(user_from = request.user, user_to = obj).delete()
                
                elif action=='request':
                    Re_quest.objects.create(user_from = request.user, user_to = obj)
                    
                elif action=='requested':
                    Re_quest.objects.get(user_from = request.user, user_to = obj).delete()
                    

                return JsonResponse({'status': 'ok', 'user_followers': obj.followers.count(), 'user_followings': obj.following.count(),\
                                        'my_requests': obj.my_requests.count(), 'users_requests': obj.requests.count()})
            except:
                pass
                
        return JsonResponse({'status': 'error'})
    
    
@login_required 
def accept(request, id, identifier):
    
    if request.method=='POST':
        obj = UserProf.objects.get(id = id)
        
        if identifier == 'my_requests':
            Re_quest.objects.get(user_from = request.user, user_to = obj).delete()
            return HttpResponseRedirect(reverse('account:accept', kwargs={'id': request.user.id, 'identifier': identifier}))
            
        elif identifier == 'users_requests':
            typee = request.POST.get('users_requests')
            
            if typee =='accept':
                Contact.objects.create(user_from = obj, user_to = request.user)
 
            Re_quest.objects.get(user_from = obj, user_to = request.user).delete() 
            return HttpResponseRedirect(reverse('account:accept', kwargs={'id': request.user.id, 'identifier': identifier}))
                
    else:
        obj = UserProf.objects.get(id = id)
        if identifier=='my_requests':
            return render(request, 'account/requests.html', {'requests': obj.my_requests.all(), 'req': 'my_req'})
        elif identifier=='users_requests':
            return render(request, 'account/requests.html', {'requests': obj.requests.all(), 'req': 'user_req'})
    
    
    
    
@login_required 
def followerings(request, id, identifier=None):
    
    if request.method=='POST':
        obj = get_object_or_404(UserProf, id=id, is_active=True)
        req = request.POST.get('req')
        
        if req == 'remove':
            Contact.objects.get(user_from = obj, user_to = request.user).delete()
            return HttpResponseRedirect(reverse('account:followerings', kwargs={'id': request.user.id, 'identifier': 'followers'}))
            
        elif req == 'unfollow':
            
            Contact.objects.get(user_from = request.user, user_to = obj).delete()
            return HttpResponseRedirect(reverse('account:followerings', kwargs={'id': request.user.id, 'identifier': 'following'}))
                
    else:
        obj = UserProf.objects.get(id = id)
        if identifier=='followers':
            return render(request, 'account/followerings.html', {'obj': obj, 'req': 'followers'})
        elif identifier=='following':
            return render(request, 'account/followerings.html', {'obj': obj, 'req': 'following'})
    
    
    
    
def register(request):

    if request.method=='POST':
        userform = createuserform(data=request.POST, files=request.FILES)

        if userform.is_valid():
                new_user = userform.save(commit=False)
                new_user.set_password(userform.cleaned_data['password1'])
                new_user.prof_image = userform.cleaned_data['prof_image']
                new_user.save()
                return render(request, 'account/register_done.html', {'new_user': new_user,
                                                    'loginform': LoginForm(),
                                                    'registerform': createuserform()})
            

    return render(request, 'account/register.html', {
                                                    'loginform': LoginForm(),
                                                    'registerform': createuserform()})


    
def changepass(request):
   if request.method=='POST':
      if request.user.is_authenticated:
            if request.POST['password1']==request.POST['password2']:
              user = UserProf.objects.get(id=request.user.id)
              user.set_password(request.POST['password1'])
              user.save()
              login(request, user)  # if you don't include this line, after changing password, you will be logged out !! .  so before going to HOME page, you should log in by this code :)
              return redirect('/')
            else:
                return redirect('/')
	
      else:
          return redirect('login')
   else:
          return render(request, 'account/changepassword.html' , {'form': changepassform()})
     
     
     
def user_login(request):
    if request.method=='POST':
            user =authenticate(request, username=request.POST['username'], password=request.POST['password'])
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.POST.get('next') == '':    # when user come from base template, value of The next parameter is '', and after login, no next page is unknown! 
                                                            #then, we assign '/' to page to redirecting to base template! if next parameter is another values! so e.x: next = /profile/4/
                        page = '/'
                        return redirect(page)
                    else:
                        return redirect(request.POST.get('next'))
                    
                else :
                    return HttpResponse('User is not active!')
                    
            else:
                return HttpResponse('user doesn\'t exist !')
                
    else:
        print(request.GET.get('next'))
        return render(request, 'account/login.html', {'form': LoginForm()})
    
    
def loggedout(request):
    
    request.user.last_logedout = timezone.now()
    request.user.save()
    logout(request)
    return redirect('/')