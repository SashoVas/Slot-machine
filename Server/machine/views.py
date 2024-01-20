from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from machine.models import User
from machine.serializers import UserSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

# Create your views here.


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test(request):
    res = {"a": 1}
    return Response(res)


@api_view(["POST"])
def login_user(request):
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response({"error": "Wrong password"})
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(user)
    return Response(
        {
            "token": token.key,
            "user": serializer.data,
        }
    )


@api_view(["POST"])
def logout_user(request):
    request.user.auth_token.delete()
    return Response({"success": "Successfully logged out."})


@api_view(["POST"])
def register_user(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        return Response(serializer.data)
    return Response(serializer.errors)
