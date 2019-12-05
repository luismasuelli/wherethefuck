from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly


class AuthenticatedAPIView(APIView):
    """
    This view authenticates via either token or session.
    """

    authentication_classes = (TokenAuthentication,)


class LoginRequiredAPIView(AuthenticatedAPIView):
    """
    This view, aside from authenticating via either token or session, requires a user to be
      already logged in.
    """

    permission_classes = (IsAuthenticated,)


class LoginPartiallyRequiredAPIView(AuthenticatedAPIView):
    """
    This view, aside from authenticating via either token or session, requires a user to be
      already logged in for non-GET/HEAD/OPTIONS operations.
    """

    permission_classes = (IsAuthenticatedOrReadOnly,)
