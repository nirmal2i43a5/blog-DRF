#Here I am creating own custom permission that allow other user what method is granted in blog

from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsOwnerOrReadOnly(BasePermission):
    message = 'You must be the owner of this object.'
    
    my_safe_method = ['GET','PUT']#only this method is allowed to other user by the owner
    
    def has_permission(self, request, view):#it overrides the method insid the base permission
        if request.method in self.my_safe_method:
            return True
        return False

    def has_object_permission(self, request, view, obj):#it overrides the method insid the base permission
        #obj_user = Model.objects.get(user=request.user)
        #obj_user.is_active#u can this this sorts of stuff to make permision more effective
        
        if request.method in SAFE_METHODS:#default ==> SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            return True
        return obj.user == request.user#obj.user comes from the models