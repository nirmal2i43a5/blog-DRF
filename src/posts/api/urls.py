from django.conf.urls import url



from .views import (
 
    PostListAPIView,
    PostDetailApiView,
    PostUpdateAPIView,
    PostDestroyAPIView,
    PostCreateAPIView
 
    )



urlpatterns = [
     url(r'^$', PostListAPIView.as_view(), name='list'),
        url(r'^(?P<slug>[\w-]+)/$', PostCreateAPIView.as_view(), name='create'),
    # url(r'^(?P<pk>\d+)/$', PostDetailApiView.as_view(), name='detail'),#when using pk 
     url(r'^(?P<slug>[\w-]+)/$', PostDetailApiView.as_view(), name='detail'),
    url(r'^(?P<slug>[\w-]+)/edit/$', PostUpdateAPIView.as_view(), name='update'),
    url(r'^(?P<slug>[\w-]+)/delete/$', PostDestroyAPIView.as_view(), name='delete'),
]
