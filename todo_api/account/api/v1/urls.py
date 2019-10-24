from django.urls import path,include
from . import views


app_name    = 'account_api'


urlpatterns = [
    path('auth/user/',views.UserAPI.as_view(),name='auth-user-api'),

    # Extra
    path('auth/users/<int:pk>/',views.UserRetrieveUpdateAPIView.as_view(),name='auth-user-profile'),
    path('auth/users/<int:pk>/delete/',views.UserDestroyAPIView.as_view(),name='auth-user-delete'),

    path('auth/users/',views.UsersListAPIView.as_view(),name='auth-users'),
    path('auth/register/',views.UserRegistrationAPIView.as_view(),name='auth-user-register'),
    path('auth/login/',views.UserLoginAPIView.as_view(),name='auth-user-login'),
    path('auth/tokens/<key>/',views.UserTokenAPIView.as_view(),name='auth-user-token'),


]
 