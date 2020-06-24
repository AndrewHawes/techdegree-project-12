from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, register_converter

from . import ajax, converters, views

register_converter(converters.UIDB64Converter, 'uidb64')
register_converter(converters.TokenConverter, 'token')

urlpatterns = [
    path('signin/', LoginView.as_view(template_name='accounts/signin.html'),
         name='signin'),
    path('signout/', LogoutView.as_view(), name='signout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name='profile'),
    path('profile_edit/', views.ProfileEditView.as_view(), name='profile_edit'),
    path('account_activation_sent/', views.account_activation_sent,
         name='account_activation_sent'),
    path('activate/<uidb64:uidb64>/<token:token>/', views.activate, name='activate')
]

ajax_urlpatterns = [
    path('get_markdown/', ajax.get_markdown, name='get_markdown'),
    path('toggle_markdown/', ajax.toggle_markdown, name='toggle_markdown'),
]

urlpatterns += ajax_urlpatterns
