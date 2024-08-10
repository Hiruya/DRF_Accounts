from django.urls import path

from .views import LoginView, LogoutView, RegisterStep1View, RegisterStep2View, RegisterStep3View, UpdateProfileView, UpdateUserView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register1/', RegisterStep1View.as_view(), name='register_step_1'),
    path('register2/', RegisterStep2View.as_view(), name='register_step_2'),
    path('register3/', RegisterStep3View.as_view(), name='register_step_3'),
    path('update-user/', UpdateUserView.as_view(), name='update_user'),
    path('update-profile/', UpdateProfileView.as_view(), name='update_profile'),
]