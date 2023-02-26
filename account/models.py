from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

 
    
class UserProf(AbstractUser):
    is_public     = models.BooleanField(default = True)
    prof_image    = models.ImageField(upload_to = 'static/images_prof', default = 'images/image_not_found.jpg')   # if add blank=True and null=True, a checkbox called clear is appear in form.
    biography     = models.TextField()
    
    last_logedout = models.DateTimeField(blank= True, null = True)
    
    def get_absolute_url(self):
        return reverse('account:user_profile', args=[self.id])
    
    def __str__(self):
        return self.username

class Contact(models.Model):
    user_from = models.ForeignKey(UserProf, related_name='rel_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey(UserProf, related_name='rel_to', on_delete=models.CASCADE)
    
    created = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f'{self.user_from} followed {self.user_to}'
        
    class Meta:
        ordering = ('-created',)

UserProf.add_to_class('following', models.ManyToManyField('self', through = Contact, related_name = 'followers', symmetrical = False))


############################################################
#########                                       ############
#########           request to follow           ############
#########                                       ############
############################################################

class Re_quest(models.Model):
    user_from = models.ForeignKey(UserProf, related_name='req_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey(UserProf, related_name='req_to', on_delete=models.CASCADE)
    
    created = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f'{self.user_from} requested to {self.user_to}'
        
    class Meta:
        ordering = ('-created',)
        
        
UserProf.add_to_class('my_requests', models.ManyToManyField('self', through = Re_quest, related_name = 'requests', symmetrical = False))         # my_requests: i requested to other users  ///  requests: users requested to me.

############################################################
#########                                       ############
#########                                       ############
#########                                       ############
############################################################

class Blocking(models.Model):
    user_from = models.ForeignKey(UserProf, related_name='block_from', on_delete=models.CASCADE)
    user_to = models.ForeignKey(UserProf, related_name='block_to', on_delete=models.CASCADE)
    
    created = models.DateTimeField(auto_now_add = True)
    
    def __str__(self):
        return f'{self.user_from} blocked {self.user_to}'
        
    class Meta:
        ordering = ('-created',)
        
        
UserProf.add_to_class('my_blocks', models.ManyToManyField('self', through = Blocking, related_name = 'blocked_me', symmetrical = False))    # my_blocks: list of users that i blocked them  ///  blocked_me: users blocked me.     


############################################################
#########                                       ############
#########                                       ############
#########                                       ############
############################################################

class Direct(models.Model):
    user_from = models.ForeignKey(UserProf, related_name='write_from', on_delete=models.CASCADE)
    user_to   = models.ForeignKey(UserProf, related_name='write_to', on_delete=models.CASCADE)
    
    created   = models.DateTimeField(auto_now_add = True)
    text      = models.TextField()
    
    show      = models.BooleanField(default = True)
    
    def __str__(self):
        return f'{self.user_from} writes to {self.user_to}'
        
    class Meta:
        ordering = ('-created',)
        
        
UserProf.add_to_class('my_directs', models.ManyToManyField('self', through = Direct, related_name = 'directs_me', symmetrical = False))