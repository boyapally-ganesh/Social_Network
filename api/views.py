from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from .models import User, FriendRequest
from .serializers import*
from django.contrib.auth import authenticate
from django.utils import timezone
from datetime import timedelta
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, permissions
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.views import APIView
from .serializers import SignupSerializer, LoginSerializer, UserSerializer
from django.contrib.auth import get_user_model
from api.renderers import UserRenderer
from rest_framework import generics, permissions
#Generate Token Manually
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

User = get_user_model()

class SignupView(generics.CreateAPIView):
    renderer_classes = [UserRenderer]
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]



   
class LoginView(ObtainAuthToken):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.validated_data.get('email')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=email, password=password)

            if user is not None:
                if user.is_active:
                    token = get_tokens_for_user(user)
                    return Response({'token':token,'msg': 'Login success'}, status=status.HTTP_200_OK)
                else:
                    return Response({'errors': {'non_field_errors': ['User account is disabled']}}, status=status.HTTP_403_FORBIDDEN)
            else:
                return Response({'errors': {'non_field_errors': ['Email or password is not valid']}}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FriendRequestView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, format=None):
        # Check for rate limiting
        one_minute_ago = timezone.now() - timedelta(minutes=1)
        recent_requests_count = FriendRequest.objects.filter(
            sender=request.user,
            created_at__gte=one_minute_ago
        ).count()

        if recent_requests_count >= 3:
            return Response(
                {'error': 'You cannot send more than 3 friend requests within a minute.'},
                status=status.HTTP_429_TOO_MANY_REQUESTS
            )

        # Proceed with creating a new friend request
        serializer = FriendRequestSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(sender=request.user, status='pending')
            return Response({'message': 'Friend request sent successfully'}, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        # List all users except the logged-in user
        users = User.objects.exclude(id=request.user.id)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserSearchPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class UserSearchView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    pagination_class = UserSearchPagination

    def get_queryset(self):
        queryset = User.objects.all()
        search_keyword = self.request.query_params.get('search', None)

        if search_keyword:
            # Search for exact email match
            email_matches = queryset.filter(email__iexact=search_keyword)
            if email_matches.exists():
                return email_matches
            
            # Search for partial name matches
            name_matches = queryset.filter(name__icontains=search_keyword)
            return name_matches

        # Return an empty queryset if no search keyword is provided
        return queryset.none()



class FriendListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer

    def get_queryset(self):
        user = self.request.user

        # Find users who have accepted the current user's friend request or vice versa
        sent_requests = FriendRequest.objects.filter(sender=user, status='accepted').values_list('receiver', flat=True)
        received_requests = FriendRequest.objects.filter(receiver=user, status='accepted').values_list('sender', flat=True)

        # Combine both sets of IDs and fetch user objects
        friend_ids = set(sent_requests).union(set(received_requests))
        friends = User.objects.filter(id__in=friend_ids)
        return friends


class PendingFriendRequestsView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def get_queryset(self):
        user = self.request.user
        # Query pending friend requests received by the current user
        pending_requests = FriendRequest.objects.filter(receiver=user, status='pending')
        return pending_requests

class UpdateFriendRequestView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FriendRequestSerializer

    def update(self, request, *args, **kwargs):
        try:
            # Find the specific friend request
            friend_request = FriendRequest.objects.get(id=kwargs['pk'], receiver=request.user)
        except FriendRequest.DoesNotExist:
            return Response({'error': 'Friend request not found.'}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve action from request data
        action = request.data.get('action', '').lower()
        if action not in ['accept', 'reject']:
            return Response({'error': 'Invalid action.'}, status=status.HTTP_400_BAD_REQUEST)

        # Update the status of the friend request
        friend_request.status = 'accepted' if action == 'accept' else 'rejected'
        friend_request.save()

        return Response({'message': f'Friend request {action}ed successfully.'}, status=status.HTTP_200_OK)

