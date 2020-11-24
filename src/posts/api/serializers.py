from rest_framework.serializers import (
    ModelSerializer,
    HyperlinkedIdentityField,
    SerializerMethodField#use for showing username instead of id
)
from posts.models import Post
from comments.api.serializers import CommentSerializer 
from comments.models import Comment
class PostCreateUpdateSerializer(ModelSerializer):#use for both create and update
    class Meta:
        model = Post
        fields = [
            #'id',
            'title',
            #'slug',
            'content',
            'publish'
        ]


#to make this see the models and make akin to that
class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'user',
            'id',
            'title',
            'slug',
            'content',
            'publish'
            
        )
        
#use this to override  easily
edit_detail_url = HyperlinkedIdentityField(
        view_name='posts-api:update',#where to go
        lookup_field = 'slug'##id is default but here we use slug
    )
list_detail_url = HyperlinkedIdentityField(
        view_name='posts-api:detail',#where to go
        lookup_field = 'slug'##id is default but here we use slug
    )
#create url in list(for hyperlink restframework doce inside relation serializers)
class PostListSerializer(ModelSerializer):
    #it shows link (I can also implement this in update and delete also acc to view_name)
    url = list_detail_url
    edit_url = edit_detail_url
    user = SerializerMethodField()
    
    class Meta:
        model = Post
        fields = (
            'url',
            'user',
            'id',
            'title',
            # 'slug',
            'content',
            'publish',
            'edit_url'
            
        )
    def get_user(self,obj):#it shows username instead of id
        return str(obj.user.username)
        
        
class PostDetailSerializer(ModelSerializer):#I can also use PostListSerializer for detail also but it is better to make separate
    
    url = HyperlinkedIdentityField(
        view_name='posts-api:delete',#where to go
        lookup_field = 'slug'##id is default but here we use slug
    )
    post = Post.objects.all()
    user = SerializerMethodField()
    image = SerializerMethodField()
  
    comments = SerializerMethodField()
    class Meta:
        model = Post
        fields = (
            'url',
            'user',
            'id',
            'title',
            'slug',
            'content',
            'publish',
            'image',
            'comments'
            
        )
        
    def get_user(self,obj):#it shows username instead of id
        return str(obj.user.username)
    
    def get_image(self,obj):#obj incorporate Post
        #show image url
        try:
            return obj.image.url
        except:
            image = None
        return image
 

    def get_image(self, obj):
        try:
            image = obj.image.url
        except:
            image = None
        return image

    def get_comments(self, obj):
        c_qs = Comment.objects.filter_by_instance(obj)
        comments = CommentSerializer(c_qs, many=True).data
        return comments
