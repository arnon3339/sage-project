from django.urls import path
# from .views import Home, UserRegistrationView
from .views.auth_views import Home, UserRegistrationView
from .views.link_view import (
    UserInfoView, FavLink, FavlinkDeleteView, FavlinkUpdateView, FavlinkEditView,
    FavlinkExistView, FavlinkKeywordView
    )

urlpatterns = [
    path('', Home.as_view()),
    path('api/auth/signup/', UserRegistrationView.as_view(), name='signup'),
    path('api/link/user/', UserInfoView.as_view(), name='link-user'),
    path('api/link/fav/', FavLink.as_view(), name='link-fav'),
    path('api/link/del/<str:kind>/', FavlinkDeleteView.as_view(), name='link-fav-del'),
    path('api/link/update/', FavlinkUpdateView.as_view(), name='link-fav-del'),
    path('api/link/edit/', FavlinkEditView.as_view(), name='link-fav-edit'),
    path('api/link/views/<str:kind>', FavlinkExistView.as_view(), name='link-fav-views'),
    path('api/link/search/', FavlinkKeywordView.as_view(), name='link-fav-search'),
]