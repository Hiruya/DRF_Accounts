from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from .views import LoginView, LogoutView, RegisterView, UpdateProfileView, UpdateUserView, register_view, login_view


urlpatterns = [
    path('api_login/', LoginView.as_view(), name='api-login'),
    path('login/', login_view, name='api-login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api_register/', RegisterView.as_view(), name='api-register'),
    path('register/', register_view, name='register'),
    # path('api_register2/', RegisterStep2View.as_view(), name='api-register2'),
    # path('register2/', register2_view, name='register2'),
    # path('register3/', RegisterStep3View.as_view(), name='register_step_3'),
    path('update-user/', UpdateUserView.as_view(), name='update_user'),
    path('update-profile/', UpdateProfileView.as_view(), name='update_profile'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)