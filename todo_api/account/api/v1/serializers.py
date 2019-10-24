from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

from rest_framework.authtoken.models import Token

from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    """ Model Serializer for app users details,works like forms.ModelForm """
    class Meta:
        model       = User
        fields      = ['pk','username','email']




class UserRegisterSerializer(serializers.ModelSerializer):
    """ User Register Serializer."""
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "username", "email", "password", "confirm_password")
    
    # def validate_email(self,email:str):
    #     pass


    # def validate_username(self,username:str):
    #     pass


    # def validate_password(self,password:str):
    #     pass

    def validate(self, attrs:dict)-> dict:
        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError("Those passwords don't match.")
        del attrs['confirm_password']
        if User.objects.filter(email__iexact = attrs.get('email')).exists():
            raise serializers.ValidationError("Email is already taken.")
        attrs['password'] = make_password(attrs['password'])

        return attrs




class UserLoginSerializer(serializers.Serializer):
    """User Login Serializer."""
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    default_error_messages = {
        'inactive_account': ('User account is disabled.'),
        'invalid_credentials': ('Unable to login with provided credentials.')
    }

    def __init__(self, *args, **kwargs):
        super(UserLoginSerializer, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self, attrs):
        self.user = authenticate(username=attrs.get("username"), password=attrs.get('password'))
        if self.user:
            if not self.user.is_active:
                raise serializers.ValidationError(self.error_messages['inactive_account'])
            return attrs
        else:
            raise serializers.ValidationError(self.error_messages['invalid_credentials'])



class TokenSerializer(serializers.ModelSerializer):
    """ Token Serializer,keep histroy of all tokens generated for users."""
    auth_token = serializers.CharField(source='key')

    class Meta:
        model = Token
        fields = ("auth_token", "created")

