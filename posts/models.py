from django.db import models
from account.models import UserProf

class Post(models.Model):
    author        = models.ForeignKey(UserProf, on_delete=models.CASCADE, related_name='posts')
    image        = models.ImageField(upload_to='static/posts_by_{self.author.username}/')
    caption       = models.TextField()

    created      = models.DateTimeField(auto_now_add = True)
    updated     = models.DateTimeField(auto_now=True)

    users_like  = models.ManyToManyField(UserProf, related_name='posts_liked', blank=True)
    views         = models.PositiveIntegerField(default=0)
    showing     = models.BooleanField(default = True)
    
    
    def __str__(self):
        return f'posted "{self.id}" by {self.author.username} on {self.created}'
        
    def get_absolute_url(self):
        return reverse('posts:post_detail', args=[self.id])

class Comment(models.Model):
    owner       = models.ForeignKey(UserProf, on_delete=models.CASCADE, related_name='user_comments')
    post          = models.ForeignKey(Post, on_delete = models.CASCADE, related_name ='post_comments')
    body        = models.TextField()
    created     = models.DateTimeField(auto_now_add = True)
    
    active      = models.BooleanField(default=True)   ##
  
    
    def __str__(self):
        return f' commented by {self.owner} on {self.post}'
        
    class Meta:
        ordering = ('created',)


class Reply(models.Model):
    user    = models.ForeignKey(UserProf, on_delete=models.CASCADE, related_name='user_replies')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_replies')
    
    text    = models.TextField()  # blank=True
    created_date = models.DateTimeField(auto_now_add = True)
    actuve  = models.BooleanField(default=True)
    
    def __str__(self):
        return f' {self.user} replied to {self.comment}'

