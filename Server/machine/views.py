from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from machine.models import User,Roll
from machine.serializers import UserSerializer,RollSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from machine import slot_machine_settings
from machine.slot_machine import Slot_machine
# Create your views here.


@api_view(["GET"])
def get_rules(request):
    return Response(
        {
            "number_to_symbol_mapping": slot_machine_settings.NUMBERS_TO_SYMBOLS_MAPPING,
            "paytable": slot_machine_settings.PAYTABLE,
            "winning_lines": slot_machine_settings.WINNING_LINES,
            "wild_symbol": slot_machine_settings.WILD_SYMBOL,
        }
    )


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test(request):
    serialiser = UserSerializer(request.user)
    return Response(serialiser.data)


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

@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def spin_machine(request):
    #if request.data["cost"] > request.user.balance:
    #    return Response({"error": "Not enough money"})
    #if request.data["cost"] <= 0:
    #    return Response({"error": "Invalid bet"})

    slot_machine=Slot_machine()
    multyplier, roll_board, winning_lines=slot_machine.roll_machine()
    board_info={"roll_board":roll_board,"winning_lines":winning_lines}
    print(board_info)

    data = {
        'user':request.user.pk,
        'cost':request.data["cost"],
        'board_info':board_info,
        'winings_multyplier':multyplier,
    }
    serializer=RollSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        #request.user.balance += roll.result
        #request.user.save()
        return Response(serializer.data)
    return Response(serializer.errors)