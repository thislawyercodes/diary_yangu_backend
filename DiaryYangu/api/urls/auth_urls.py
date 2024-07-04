from django.urls import path

from api.views import CustomTokenObtainPairView, UserCreateView,UserProfileDetail,UserProfileDeactivate


app_name="Auth"


urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('register/', UserCreateView.as_view(), name='user_create'),
    path('profile/<str:user_id>', UserProfileDetail.as_view(), name='user_profile'),
    path('user/deactivate/<str:user_id>', UserProfileDetail.as_view(), name='user_profile'),

]
