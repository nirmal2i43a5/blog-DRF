from django.conf.urls import url
from django.contrib import admin

from .views import (
    CommentCreateAPIView,
    CommentDetailAPIView,
    CommentListAPIView,
  

    )

urlpatterns = [
    url(r'^$', CommentListAPIView.as_view(), name='list'),
    url(r'^create/$', CommentCreateAPIView.as_view(), name='create'),
    
    # for creating use url like => api/comments/create/?type=post&slug=python (i cannot create just using api/comments/create/ because It lags ideas to which post i want to create comment )
    
    url(r'^(?P<pk>\d+)/$', CommentDetailAPIView.as_view(), name='thread'),
    #    url(r'^(?P<pk>\d+)/edit/$', CommentEditAPIView.as_view(), name='edit'),
    #url(r'^(?P<id>\d+)/delete/$', comment_delete, name='delete'),
]