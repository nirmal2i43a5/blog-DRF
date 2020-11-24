from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import get_user_model

from rest_framework.serializers import (
    HyperlinkedIdentityField,
    ModelSerializer,
    SerializerMethodField,
    ValidationError
    )

from accounts.api.serializers import UserDetailSerializer

from comments.models import Comment

User = get_user_model()

def create_comment_serializer(model_type='post', slug=None, parent_id=None, user=None):#receive this args from CommentCreateAPIView  views comments/api/views.py
    print("-----------------2--------------------")
    class CommentCreateSerializer(ModelSerializer):
        class Meta:
            model = Comment
            fields = [
                'id',
                # 'parent',
                'content',
                'timestamp',
            ]
            
        #1>it initialize the comment data
        def __init__(self, *args, **kwargs):   
            self.model_type = model_type
            self.slug = slug
            self.parent_obj = None
            
            if parent_id:
                parent_qs = Comment.objects.filter(id=parent_id)
                if parent_qs.exists() and parent_qs.count() ==1:
                    self.parent_obj = parent_qs.first()
            return super(CommentCreateSerializer, self).__init__(*args, **kwargs)

        #2>it checks for  validate  contenttype and slug for that contenttype in commentform once it is submit
        def validate(self, data):
            model_type = self.model_type#right self.model_type is the instance var in above init
            model_qs = ContentType.objects.filter(model=model_type)#give content_type post
         
            
            if not model_qs.exists() or model_qs.count() != 1:
                raise ValidationError("This is not a valid content type")
            
            SomeModel = model_qs.first().model_class()
            # print(SomeModel)#<class 'posts.models.Post'> 
            obj_qs = SomeModel.objects.filter(slug=self.slug)#check slug inside model i.e Post in this case(pros of generic for other model also)
            
            if not obj_qs.exists() or obj_qs.count() != 1:
                raise ValidationError("This is not a slug for this content type")
            return data


        #it creates the comment and save to database
        def create(self, validated_data):
            content = validated_data.get("content")
            
            if user:
                main_user = user
            else:
                main_user = User.objects.all().first()
                 
            model_type = self.model_type
            slug = self.slug
            parent_obj = self.parent_obj
            print("-----------------3--------------------")
            comment = Comment.objects.create_by_model_type(
                    model_type, slug, content, main_user,
                    parent_obj=parent_obj,
                    )
            return comment#create always return object instance

    return CommentCreateSerializer#i can create class inside the function as long as i return this class


#THIS CommentSerializer IS USED IN POSTS SERIALIZERS TO SHOW COMMENTS
class CommentSerializer(ModelSerializer):
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'content_type',
            'object_id',
            'parent',
            'content',
            'reply_count',
            'timestamp',
        ]
    
    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0



class CommentListSerializer(ModelSerializer):
    url = HyperlinkedIdentityField(
        view_name='comments-api:thread')
    reply_count = SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'url',
            'id',
            # 'content_type',
            # 'object_id',
            # 'parent',
            'content',
            'reply_count',
            'timestamp',
        ]
    
    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0



class CommentChildSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'timestamp',
        ]

class CommentDetailSerializer(ModelSerializer):
    user = UserDetailSerializer(read_only=True)
    reply_count = SerializerMethodField()
    content_object_url = SerializerMethodField()
    
    replies =   SerializerMethodField()
    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            # 'content_type',
            # 'object_id',
            'content',
            'reply_count',
            'replies',
            'timestamp',
            'content_object_url',
        ]
        
        read_only_fields = [#cannot edit this field in detail view i.e only can be edited
            # 'content_type',
            # 'object_id',
            'reply_count',
            'replies',
        ]

    def get_content_object_url(self, obj):
        try:
            return obj.content_object.get_api_url()
        except:
            return None


    def get_replies(self, obj):
        if obj.is_parent:
            return CommentChildSerializer(obj.children(), many=True).data#achieve obj.children() from comment/models.py amd serialize that data
        return None

    def get_reply_count(self, obj):
        if obj.is_parent:
            return obj.children().count()
        return 0

