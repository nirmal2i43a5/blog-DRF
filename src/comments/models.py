

from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.urlresolvers import reverse
from django.db import models
# from posts.models import Post   I cannot import Post here as comment is also imported in post


class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent=None)
        return qs

    def filter_by_instance(self, instance):#receive instance from comments decorator in this same page
        content_type = ContentType.objects.get_for_model(instance.__class__)#writing Post model here is similar to instance.__class__ i.e Post = instance.__class__(using this for generic foreign key)
        #I am using instance.__class__ blc i cannot import Post from post model as comment is also imported in comment post model
        obj_id = instance.id
        qs = super(CommentManager, self).filter(content_type=content_type, object_id= obj_id).filter(parent=None)#parent is used for reply logic
        #super(CommentManager, self) means Comment.objects
        return qs
    
    #this is for comment serializers
    def create_by_model_type(self, model_type, slug, content, user, parent_obj=None):
        model_qs = ContentType.objects.filter(model=model_type)
        if model_qs.exists():
            SomeModel = model_qs.first().model_class()
            obj_qs = SomeModel.objects.filter(slug=slug)
            if obj_qs.exists() and obj_qs.count() == 1:
                instance = self.model()
                instance.content = content
                instance.user = user
                instance.content_type = model_qs.first()
                instance.object_id = obj_qs.first().id
                if parent_obj:
                    instance.parent = parent_obj
                instance.save()
                return instance
        return None

    
      #this logic is for rest api
      


      
class Comment(models.Model):
    user        = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    
    # post = models.ForeignKey(Post)#instead of using this models(which only deals with Post models) I am using generic key to make it more effective
    
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)#it deals with multiple models 
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    
    parent      = models.ForeignKey("self", null=True, blank=True,on_delete=models.CASCADE)#i need this only when i reply the comment otherwise for just comment it is not used
    #i see parent data in admin site only when i reply to particular comment
    content     = models.TextField()
    timestamp   = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

    class Meta:
        ordering = ['-timestamp']



    def __str__(self):
        return str(self.user.username)

    def get_absolute_url(self):
        return reverse("comments:thread", kwargs={"id": self.id})

    def get_delete_url(self):
        return reverse("comments:delete", kwargs={"id": self.id})
        
    def children(self): #replies
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True



