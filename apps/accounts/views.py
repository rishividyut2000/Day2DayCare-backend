from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import D2DTokenSerializer


class LoginView(TokenObtainPairView):
    serializer_class = D2DTokenSerializer
