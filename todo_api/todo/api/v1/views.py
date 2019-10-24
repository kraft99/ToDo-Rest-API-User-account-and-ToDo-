
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
)
from rest_framework.authentication import (
    SessionAuthentication,
    BaseAuthentication
)

from .permissions import IsTodoOwnerOrReadOnly
from .pagination import TodoPageNumberPagination

from .serializers import TodoAPISerializer
from todo_api.todo.models import Todo


class TodoListCreateAPIView(generics.ListCreateAPIView):
    """ View to List all instances of a Model and Create creates new instances. """
    serializer_class        = TodoAPISerializer
    pagination_class        = TodoPageNumberPagination
    permission_classes      = [IsAuthenticatedOrReadOnly,IsTodoOwnerOrReadOnly]
    # authentication_classes  = [SessionAuthentication,BaseAuthentication]
    filter_backends         = [SearchFilter,OrderingFilter]
    search_fields           = ['name']


    def get_queryset(self):
        """List all todos of a Todo Model """
        user = self.request.user
        qry = Todo.objects.all()
        # # qry = qry.filter(owner = user)
        # if user.is_authenticated and not user.is_anonymous:
        #     qry = qry.filter(owner = user) # filter by login user.
        return qry


    def get_serializer_context(self,*args,**kwargs):
        # required for instance url.
        return {'request':self.request}


    def perform_create(self,serializer):
        """ saves current user to a todo instance """
        serializer.save(owner  = self.request.user)




class TodoRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """ View to Retrieve,Update,Destroy a Model instance.
    Only todo owners can update and destroy a todo.
    but others can read only.
    
    only authenicated(tokenized users) users can see todos with [IsAuthenticated]
    [IsTodoOwnerOrReadOnly] allow users of todo perform actions - edit,delete
    only users with todo can see thier todos with ,qry.filter(owner = user)

    only only owner of todo can alter changes.
    but others can only view.

    """
    serializer_class         = TodoAPISerializer
    lookup_field             = 'pk'
    permission_classes       = [IsAuthenticatedOrReadOnly,IsTodoOwnerOrReadOnly]
    # authentication_classes   = [SessionAuthentication,BaseAuthentication]


    def get_queryset(self):
        """ List all todos of a Todo Model """
        user = self.request.user
        qry = Todo.objects.all() # list all todo's - default.
        ## if user.is_anonymous:
        ##     qry = Todo.objects.none()
        # if user.is_authenticated and not user.is_anonymous:
        #     qry = qry.filter(owner = user) # filter by login user.
        return qry

    

    def get_serializer_context(self,*args,**kwargs):
        return {'request':self.request}

    
    def perform_update(self,serializer):
        """ saves current user as the request.user to a todo instance """
        serializer.save(owner = self.request.user)
    

    
