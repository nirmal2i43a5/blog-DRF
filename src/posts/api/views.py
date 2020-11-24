from rest_framework.generics import (
                                     ListAPIView,
                                     RetrieveAPIView,
                                     RetrieveUpdateAPIView,
                                     DestroyAPIView,
                                     CreateAPIView
                                     )

from django.db.models import Q
from posts.models import Post
from .serializers import  PostListSerializer,PostDetailSerializer,PostCreateUpdateSerializer

from .permissions import IsOwnerOrReadOnly
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
    IsAdminUser,
    IsAuthenticatedOrReadOnly,#it deals with retrieve api view

    )


from rest_framework.filters import (
        SearchFilter,
        OrderingFilter,
    )

from rest_framework.pagination import PageNumberPagination,LimitOffsetPagination

from .pagination import PostLimitOffsetPagination,PostPageNumberPagination

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
    permission_classes = [IsAuthenticatedOrReadOnly ,IsOwnerOrReadOnly]




class PostListAPIView(ListAPIView):#this assists to see my data in json or api format 
    # queryset = Post.objects.all() #b4 using get_queryset i need this but after using filter it in defined inside that get_queryset
    serializer_class = PostListSerializer
    
    # ----------------------#for built in search---------------------------
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields = ['title','content','user__first_name']#this is akin to the admin search concept
    
    #builtin pagination
    # pagination_class = LimitOffsetPagination#search in url with ?limit=1 for 1 data per page and so on
    
    #custom paginaiton which also shows pagination link directly check in pagination.py
    pagination_class = PostPageNumberPagination#it shows ?offset = 2 ...in url
    
    # pagination_class = PostLimitOffsetPagination#it shows ?page = 2..in url
    
    #if i use built in search like above then i dont need to write below code
    #result with builtin search ==> api/posts/?search=title   with below ?q=title ===  (I can also use both custom and builtin and results is api/posts/?search=title&q=title)
    #Using OrderingFilter we can use api/posts/?search=java&ordering=-id(decending order for -ve..I can also order with other fields like user,title---)
   
   
    #for searching  
    def get_queryset(self, *args, **kwargs):
        #queryset_list = super(PostListAPIView, self).get_queryset(*args, **kwargs)
        queryset_list = Post.objects.all() #filter(user=self.request.user) 
        query = self.request.GET.get("q")
        
        if query:
            queryset_list = queryset_list.filter(
                    Q(title__icontains=query)|
                    Q(content__icontains=query)|
                    Q(user__first_name__icontains=query) |
                    Q(user__last_name__icontains=query)
                    ).distinct()
        return queryset_list

    #now go and search (  ?q= title name )#ex = > ?q = python 
    
class PostDetailApiView(RetrieveAPIView):#retrieve detail with its id
    queryset = Post.objects.all()
    
    serializer_class = PostDetailSerializer
    lookup_field = 'slug'#now url is like  (--- api/posts/python-beginners/)
    