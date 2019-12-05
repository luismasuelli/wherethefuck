from rest_framework import status
from rest_framework.serializers import as_serializer_error, ValidationError, DjangoValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from ..base_views import AuthenticatedAPIView
from .serializers import *
from ...models import User


class RegisterAPIView(APIView):
    """
    This is the registration endpoint. It is expected a post call with parameters
      being username, email, password and password_confirmation.
    """

    def post(self, request):
        """
        Deserializes and validates the registration data. A user will be created
          and immediately active.
        """

        serializer = RegisterSerializer(data=request.POST)
        serializer.is_valid(True)
        action = serializer.save()
        try:
            user = User(username=action.username, email=action.email)
            user.full_clean()
            user.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except (ValidationError, DjangoValidationError) as exc:
            raise ValidationError(detail=as_serializer_error(exc))
