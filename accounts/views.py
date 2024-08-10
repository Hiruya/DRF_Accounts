from django.http import Http404
from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from .serializers import Register1Serializer, Register2Serializer, UpdateUserSerializer, UpdateProfileSerializer
from .models import CustomUser, MemberProfile

User = get_user_model()

# Register Step 1: Create User
class RegisterStep1View(generics.CreateAPIView):
    
    queryset = CustomUser.objects.all()
    serializer_class = Register1Serializer
    permission_classes = [permissions.AllowAny]

# Register Step 2: Create Member Profile
class RegisterStep2View(generics.CreateAPIView):
    queryset = MemberProfile.objects.all()
    serializer_class = Register2Serializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Register Step 3: Preview Data
class RegisterStep3View(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            profile = MemberProfile.objects.get(user=user)
            data = {
                "username": user.username,
                "email": user.email,
                "full_name": profile.full_name,
                "phone_number": profile.phone_number,
                "date_of_birth": profile.date_of_birth,
                "gender": profile.gender,
                "height": profile.height,
                "weight": profile.weight,
                "medical_history": profile.medical_history,
            }
            return Response(data)
        except MemberProfile.DoesNotExist:
            return Response({"error": "Profile not found"}, status=404)

# Login
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response({"message": "Login successful"}, status=status.HTTP_200_OK)
        return Response({"message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


# Logout
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

# Update User Data (Register1 Fields)
class UpdateUserView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Update Member Profile Data (Register2 Fields)
class UpdateProfileView(generics.UpdateAPIView):
    queryset = MemberProfile.objects.all()
    serializer_class = UpdateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return MemberProfile.objects.get(user=self.request.user)
        except MemberProfile.DoesNotExist:
            raise Http404("Profile not found")

