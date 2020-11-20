from rest_framework.generics import ListAPIView,RetrieveAPIView,RetrieveUpdateAPIView,DestroyAPIView,CreateAPIView

from posts.models import Post
from .serializers import PostListSerializer,PostDetailSerializer,PostCreateUpdateSerializer

from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,#it deals with retrieve api view

    )



class PostCreateAPIView(CreateAPIView):#this assists to see my data in json or api format 
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]#can create post only when authenticated
    
    def perform_create(self,serializer):#this is builtin method
        #this create content for respective login user
        serializer.save(user = self.request.user)
            
    
class PostUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsAuthenticatedOrReadOnly ,IsOwnerOrReadOnly]#only owner can create object
    #IsOwnerOrReadOnly is the custom permission in permission.py
    
    def perform_update(self,serializer):#this is builtin method
        serializer.save(user = self.request.user)

class PostDestroyAPIView(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer
    lookup_field = 'slug' 
    

class PostListAPIView(ListAPIView):#this assists to see my data in json or api format 
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    
class PostDetailApiView(RetrieveAPIView):#retrieve detail with its id
    queryset = Post.objects.all()
    
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'#now url is like  (--- api/posts/python-beginners/)
    