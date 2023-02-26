from new_site_3 import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static 
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='base.html'), name='base'),
    path('users/', include('account.urls', namespace='account')),
    path('posts/', include('posts.urls', namespace='posts')),
    path('story/', include('story.urls', namespace='story')),
    path('chat/', include('chat.urls', namespace='chat')),
]
#+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
