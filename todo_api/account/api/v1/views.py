from rest_framework import generics
from rest_framework.permissions import (
    IsAuthenticatedOrReadOnly,
    IsAuthenticated,
    IsAdminUser,
)

from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

from rest_framework import status
from rest_framework.response import Response

from .permissions import AnonPermissionOnly,IsAccountOwnerOrReadOnly

from .serializers import UserSerializer,UserRegisterSerializer,UserLoginSerializer,TokenSerializer




class UsersListAPIView(generics.ListAPIView):
    """ view to list all users."""
    serializer_class    = UserSerializer
    queryset            = User.objects.all()
    permission_classes  = ()
    authentication_classes = ()



class UserRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """ view to read-update-delete user(s). users can update"""

    lookup_field = "pk"
    serializer_class = UserSerializer
    permission_class = (IsAccountOwnerOrReadOnly,) 


    def get_queryset(self):
        """ return list of users in app."""
        qry = User.objects.all()
        return qry


    


class UserDestroyAPIView(generics.DestroyAPIView):
    # currently not working.
    """ only admin can delete or remove users from app."""

    lookup_field = "pk"
    serializer_class = UserSerializer
    permission_class = (IsAdminUser,) 


    def get_queryset(self):
        """ return list of users in app."""
        qry = User.objects.all()
        return qry


class UserRegistrationAPIView(generics.CreateAPIView):
    """ creating new users."""
    authentication_classes = ()
    permission_classes = ()
    serializer_class = UserRegisterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        user = serializer.instance
        token, created = Token.objects.get_or_create(user=user)
        data = serializer.data
        data["token"] = token.key

        headers = self.get_success_headers(serializer.data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)


class UserLoginAPIView(generics.GenericAPIView):
    authentication_classes = ()
    permission_classes = (AnonPermissionOnly,)
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.user
            token, _ = Token.objects.get_or_create(user=user)
            return Response(
                data=TokenSerializer(token).data,
                status=status.HTTP_200_OK,
            )
        else:
            return Response(
                data=serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )


class UserAPI(generics.RetrieveAPIView):
    """ retrieves request user with given token.
    Header - Authorization
    Token  - 787473478578hsdbjfgh7848y7878hb
    """
    serializer_class    = UserSerializer

    def get_object(self):
        return self.request.user



class UserTokenAPIView(generics.RetrieveDestroyAPIView):
    """ Retreive-Destroy tokens."""

    lookup_field = "key"
    serializer_class = TokenSerializer
    queryset = Token.objects.all()

    def filter_queryset(self, queryset):
        return queryset.filter(user=self.request.user)

    def retrieve(self, request, key, *args, **kwargs):
        if key == "current":
            instance = Token.objects.get(key=request.auth.key)
            serializer = self.get_serializer(instance)
            return Response(serializer.data)
        return super(UserTokenAPIView, self).retrieve(request, key, *args, **kwargs)

    def destroy(self, request, key, *args, **kwargs):
        if key == "current":
            Token.objects.get(key=request.auth.key).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return super(UserTokenAPIView, self).destroy(request, key, *args, **kwargs)
