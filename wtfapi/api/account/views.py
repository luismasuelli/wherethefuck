from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.serializers import as_serializer_error, DjangoValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from ..base_views import AuthenticatedAPIView, LoginRequiredAPIView
from .serializers import *
from ...models import User


class RegisterAPIView(APIView):
    """
    This is the registration endpoint. It is expected a post call with parameters
      being username, email, password and password_confirmation.
    """

    def post(self, request):
        """
        De-serializes and validates the registration data. A user will be created
          and immediately active.
        """

        serializer = RegisterSerializer(data=request.POST)
        serializer.is_valid(True)
        action = serializer.save()
        try:
            user = User(username=action.username, email=action.email)
            user.full_clean()
            user.save()
            data = {
                'username': serializer.data['username'],
                'email': serializer.data['email']
            }
            return Response(data, status=status.HTTP_201_CREATED)
        except (ValidationError, DjangoValidationError) as exc:
            raise ValidationError(detail=as_serializer_error(exc))


class LoginAPIView(APIView):
    """
    This is the login endpoint. It is expected a post call with parameters being username
      and password.
    """

    def post(self, request):
        """
        De-serializes and validates the login data. A user will be matched, or perhaps not.
          Upon success, a token will be created for the logged-in user, and returned in
          an "Authorization" header.
        """

        serializer = RegisterSerializer(data=request.POST)
        serializer.is_valid(True)
        action = serializer.save()
        user = authenticate(request, username=action.username, password=action.password)
        if user:
            key = Token.objects.create(user=user).key
            return Response({'detail': 'success'}, status=status.HTTP_200_OK, headers={
                'Authorization': 'Token ' + key
            })
        else:
            return Response({'detail': 'failed'}, status=status.HTTP_401_UNAUTHORIZED)


class Logout(AuthenticatedAPIView):
    """
    This is the logout view. It essentially invalidates the given user token, if any.
    """

    def post(self, request):
        if request.auth:
            # It will be a token. Let's delete it.
            request.auth.delete()
        return Response({'detail': 'success'}, status=status.HTTP_200_OK)


class CloseAccount(LoginRequiredAPIView):
    """
    This is the close account view. It will inactivate the user, and destroy authentication.
    """

    def post(self, request):
        serializer = CloseAccountSerializer(data=request.POST)
        serializer.is_valid(True)
        action = serializer.save()
        # The user will re-authenticate just to check credentials validity.
        user = authenticate(request, username=action.username, password=action.password)
        if user:
            if request.auth:
                request.auth.delete()
            user.is_active = False
            user.save()
        return Response({'detail': 'success'}, status=status.HTTP_200_OK)
