from rest_framework.serializers import ModelSerializer
from posts.models import Post




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
        
class PostDetailSerializer(ModelSerializer):#I can also use PostListSerializer for detail also but it is better to make separate
    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'slug',
            'content',
            'publish'
            
        )
        
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
