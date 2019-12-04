from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication


class AuthenticatedAPIView(APIView):
    """
    This view authenticates via either token or session.
    """

    authentication_classes = (TokenAuthentication, SessionAuthentication)
