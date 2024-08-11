from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from .models import FriendRequest, User

# Get the custom user model. This ensures compatibility with any user model configuration.
User = get_user_model()

# Serializer for user signup
class SignupSerializer(serializers.ModelSerializer):
    # Define the password field to be write-only and require password validation
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])

    class Meta:
        # Specify the user model and the fields to be serialized
        model = User
        fields = ('email', 'name', 'password')

    def create(self, validated_data):
        # Create a new user with the provided email, name, and password
        user = User.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )
        return user

# Serializer for user login
class LoginSerializer(serializers.Serializer):
    # Define email and password fields for login
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    
    class Meta:
        # Specify the user model and the fields to be serialized
        model = User
        fields = ['email', 'password']

# Serializer for user model representation
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify the user model and the fields to be serialized
        model = User
        fields = ['id', 'email', 'name']

# Serializer for friend request operations
class FriendRequestSerializer(serializers.ModelSerializer):
    class Meta:
        # Specify the friend request model and the fields to be serialized
        model = FriendRequest
        fields = ['id', 'sender', 'receiver', 'status', 'created_at']
        # Mark sender, status, and created_at as read-only fields
        read_only_fields = ['sender', 'status', 'created_at']

    def validate_receiver(self, value):
        # Validate the receiver field in a friend request
        user = self.context['request'].user
        # Check if the user is trying to send a friend request to themselves
        if value == user:
            raise serializers.ValidationError("You cannot send a friend request to yourself.")
        # Check if a friend request has already been sent from the user to the receiver
        if FriendRequest.objects.filter(sender=user, receiver=value).exists():
            raise serializers.ValidationError("Friend request already sent.")
        return value
