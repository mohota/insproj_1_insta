from django.db import models
from account.models import UserProf
from django.urls import reverse


class StoryModel(models.Model):
    owner = models.ForeignKey(UserProf, related_name = 'stories', on_delete = models.CASCADE)
    image = models.ImageField(upload_to = 'static/stories')
    
    viewers = models.ManyToManyField(UserProf, related_name = 'viewed_stories', blank = True)
    created = models.DateTimeField(auto_now_add = True, db_index=True)

    class Meta:
        ordering = ('-created',)
        
    def get_absolute_url(self):
        return reverse('story:', kwargs={'id': self.id})
    
    def __str__(self):
        return f'{self.owner.username} add this story at {self.created}'