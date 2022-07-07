from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, Request, Response, status

from users.models import User
from users.permissions import UserPermission
from users.serializers import LoginSerializer, UserSerializer


class UserView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermission]


    def get(self, _: Request):
        users = User.objects.all()
        serialized = UserSerializer(users, many=True)

        return Response(serialized.data, status.HTTP_200_OK)

    def post(self, request: Request):
        serialized = UserSerializer(data=request.data)

        serialized.is_valid(raise_exception=True)
        serialized.save()

        return Response(serialized.data, status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request: Request):
        serialized = LoginSerializer(data=request.data)
        serialized.is_valid(raise_exception=True)

        user: User = authenticate(**serialized.validated_data)

        if not user:
            return Response(
                {"detail": "Invalid credentials."}, status.HTTP_401_UNAUTHORIZED
            )

        token, _ = Token.objects.get_or_create(user=user)

        return Response({"token": token.key}, status.HTTP_200_OK)

class UsersView(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermission]

    def get(self, _: Request):

        users = User.objects.all()
        serialized = UserSerializer(instance=users, many=True)

        return Response({
            "users": serialized.data
        }, status.HTTP_200_OK)

class UserViewDetail(APIView):

    authentication_classes = [TokenAuthentication]
    permission_classes = [UserPermission]

    def get(self, request, user_id):

        user = get_object_or_404(User, pk=user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)