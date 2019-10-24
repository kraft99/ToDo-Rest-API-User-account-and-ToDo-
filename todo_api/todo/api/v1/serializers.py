from django.contrib.humanize.templatetags import humanize
from django.contrib.auth.models import User

from rest_framework.reverse import reverse as api_reverse

from todo_api.account.api.v1.serializers import UserSerializer

from rest_framework import serializers
from todo_api.todo.models import Todo



# Todo Model

# owner    = models.ForeignKey(to = get_user_model(),on_delete=models.CASCADE)
# name     = models.CharField(max_length=60)
# is_done  = models.BooleanField(default=False)

class TodoAPISerializer(serializers.ModelSerializer):
    """ Todo Serializer Model."""

    created_naturaltime     = serializers.SerializerMethodField(read_only=True)
    is_owner                = serializers.SerializerMethodField()
    owner                   = UserSerializer(read_only=True) # import and use UserSerializer,serializes owner field
    url                     = serializers.SerializerMethodField(read_only=True)
    uri                     = serializers.SerializerMethodField(read_only=True)
    is_authenticated_user   = serializers.SerializerMethodField()
    class Meta:
        model               =   Todo
        fields              =   ['pk','url','uri','owner','name','is_done','created_naturaltime','is_owner','is_authenticated_user']
        read_only_fields    =   ['created','updated']


    def get_created_naturaltime(self,obj):
        """ utility method for a human readable time eg. 23 minutes ago"""
        todo_instance = obj
        return humanize.naturaltime(todo_instance.created)


    def get_url(self,obj):
        # remove this approach by cfe. models. and views def get_serializer_context() method.
        """ instance url ie. http://127.0.0.1:8000/api/v1/todos/id/ , id = 1,2 ... """
        todo_instance = obj
        request = self.context.get('request')
        return todo_instance.get_api_url(request = request)


    def get_uri(self,obj):
        # approach to get uri or url, better than cfe guide.
        """ instance url ie. http://127.0.0.1:8000/api/v1/todos/id/ , id = 1,2 ... """
        request  = self.context.get('request')
        return api_reverse('todo_api:todo-detail',kwargs={'pk':obj.pk},request=request)


    def get_is_owner(self,obj):
        """ check if user is owner of todo """
        todo_instance = obj
        user    = None
        request = self.context.get('request')
        if request and hasattr(request,'user'):
            user  = request.user
        if user == todo_instance.owner:
            return True
        return False

    def get_is_authenticated_user(self,obj):
        """ checking to see user is authenticated."""
        request = self.context.get('request')
        if request.user.is_authenticated:
            return True
        return False


    def validate(self,response_data): # clean
        # validate incoming data - (name) ,form.is_valid() in ModelForm
        todo_name   = response_data.get('name',None)
        if todo_name is None:
            raise serializers.ValidationError("Todo name is required.")
        if len(todo_name) < 5:
            raise serializers.ValidationError("Todo name is too short.")
        return response_data
    

    # def validate_name(self,req_field):# clean_name
    #     pass



