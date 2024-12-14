from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .models import VerificationCode, CustomerUser, BaseUser
from .serializers import (
    SendVerificationCodeSerializer,
    VerifyCodeSerializer,
    RegisterCustomerSerializer,
    RegisterProviderSerializer,
    LoginSerializer,
    LogoutSerializer,
    RefreshTokenSerializer,
    UserDetailSerializer,
)
import random

class SendVerificationCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendVerificationCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']

            # Check if the user already exists
            if BaseUser.objects.filter(phone_number=phone_number).exists():
                return Response(
                    {'status': 'error', 'message': 'User with this phone number already exists.'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            code = str(random.randint(100000, 999999))  # Generate a 6-digit code
            print(f'code: {code}')
            VerificationCode.objects.create(phone_number=phone_number, code=code)
            # In production, send the code via SMS here
            return Response({'status': 'success', 'message': 'Verification code sent successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = VerifyCodeSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            code = serializer.validated_data['code']
            try:
                verification_code = VerificationCode.objects.get(
                    phone_number=phone_number, code=code, is_used=False
                )
                verification_code.is_used = True
                verification_code.save()
                return Response({'status': 'success', 'message': 'Verification successful.', 'phone_number': phone_number})
            except VerificationCode.DoesNotExist:
                return Response({'status': 'error', 'message': 'Invalid or expired verification code.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterBuyerView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterCustomerSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': 'success', 'message': 'Buyer registered successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterProviderView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterProviderSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'status': 'success', 'message': 'Provider registered successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            try:
                user = CustomerUser.objects.get(phone_number=phone_number) # TODO: change to BaseUser
                if user.check_password(password):
                    tokens = RefreshToken.for_user(user)
                    return Response({
                        'status': 'success',
                        'access': str(tokens.access_token),
                        'refresh': str(tokens),
                    })
                else:
                    raise BaseUser.DoesNotExist
            except BaseUser.DoesNotExist:
                return Response({'status': 'error', 'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(data=request.data)
        if serializer.is_valid():
            refresh_token = serializer.validated_data['refresh']
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
                return Response({'status': 'success', 'message': 'Logged out successfully.'})
            except Exception:
                return Response({'status': 'error', 'message': 'Invalid or expired refresh token.'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenView(TokenRefreshView):
    serializer_class = RefreshTokenSerializer


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserDetailSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
