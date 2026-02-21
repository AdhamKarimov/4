from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import SignUpSerializer , ProfileSerializer ,ProfilUdateSerializers,PasswordChangeSerializer
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token


class SignUpView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        response = {
            'status': status.HTTP_201_CREATED,
            'message': user.username
        }
        return Response(response)


class LoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        username = self.request.data.get('username')
        password = self.request.data.get('password')

        user = authenticate(username=username, password=password)

        if not user:
            raise ValidationError({'message': 'Username yoki parol notogri'})

        token, _ = Token.objects.get_or_create(user=user)

        response = {
            'status': status.HTTP_201_CREATED,
            'message': 'Siz ruxatdan otdingiz',
            'token': str(token.key)
        }
        return Response(response)


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        request.user.auth_token.delete()
        response = {
            'status': status.HTTP_200_OK,
            'message': 'Siz muvofaqqiyatli lagout qildingiz',
        }
        return Response(response)


class ProfileView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user
        serializer = ProfileSerializer(user)

        response = {
            'status': status.HTTP_200_OK,
            'malumot': serializer.data
        }
        return Response (response)

class UserProfileView(APIView):
    permission_classes=(IsAuthenticated,)
    def patch(self, request):
        user = request.user
        serializer = ProfilUdateSerializers(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = {
            'status': status.HTTP_200_OK,
            'message': "malumotingiz o'zgardi"
        }
        return Response(response)


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status


class PasswordChangeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer =PasswordChangeSerializer (data=request.data)

        if serializer.is_valid():
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {"old_password": "Eski parol noto'g'ri kiritildi."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user.set_password(serializer.validated_data['new_password'])
            user.save()

            return Response({"message": "Parol muvaffaqiyatli yangilandi."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)