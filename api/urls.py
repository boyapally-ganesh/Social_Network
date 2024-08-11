from django.urls import path
from .views import SignupView, LoginView, FriendRequestView, UserSearchView, FriendListView, PendingFriendRequestsView, UpdateFriendRequestView

urlpatterns = [
     path('signup/', SignupView.as_view(), name='signup'),
     path('login/', LoginView.as_view(), name='login'),
     path('friend-request/', FriendRequestView.as_view(), name='friend-request'),
     path('search/', UserSearchView.as_view(), name='user-search'),
     path('friends/', FriendListView.as_view(), name='friends-list'),
     path('pending-requests/', PendingFriendRequestsView.as_view(), name='pending-requests'),
     path('update-request/<int:pk>/', UpdateFriendRequestView.as_view(), name='update-friend-request'),
]