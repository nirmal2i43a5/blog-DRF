from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField
from posts.models import Post


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

#create url in list(for hyperlink restframework doce inside relation serializers)
class PostListSerializer(ModelSerializer):
    #it shows link (I can also implement this in update and delete also acc to view_name)
    url = HyperlinkedIdentityField(
        view_name='posts-api:detail',#where to go
        lookup_field = 'slug'##id is default but here we use slug
    )
   
    edit_url = edit_detail_url
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
        
        
        
class PostDetailSerializer(ModelSerializer):#I can also use PostListSerializer for detail also but it is better to make separate
    
    url = HyperlinkedIdentityField(
        view_name='posts-api:delete',#where to go
        lookup_field = 'slug'##id is default but here we use slug
    )
    class Meta:
        model = Post
        fields = (
            'url',
            'id',
            'title',
            'slug',
            'content',
            'publish'
            
        )
        
