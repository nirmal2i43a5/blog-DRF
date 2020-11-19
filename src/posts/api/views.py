from rest_framework.generics import ListAPIView

from posts.models import Post
from .serializers import PostSerializer

class PostListAPIView(ListAPIView):#this assists to see my data in json or api format 
    
    queryset = Post.objects.all()
    
    serializer_class = PostSerializer
    