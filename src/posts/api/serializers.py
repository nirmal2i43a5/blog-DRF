from rest_framework.serializers import ModelSerializer
from posts.models import Post

#to make this see the models and make akin to that
class PostSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            'id',
            'title',
            'slug',
            'content',
            'publish'
            
        )