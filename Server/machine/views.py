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
from statistics import stdev
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
def user_info(request):
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


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_history(request):
    rolls = Roll.objects.filter(user=request.user)
    serializer = RollSerializer(rolls, many=True)
    return Response(serializer.data)

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_statistics(request):
    rolls = Roll.objects.filter(user=request.user)
    total_amoounth_won=sum([roll.result for roll in rolls])
    total_amount_bet=sum([roll.cost for roll in rolls])
    max_amount_won=max([roll.result for roll in rolls])
    max_amount_bet=max([roll.cost for roll in rolls])
    total_spins=len(rolls)
    profit=total_amoounth_won-total_amount_bet
    amount_won_per_spin=total_amoounth_won/total_spins
    average_bet=total_amount_bet/total_spins
    std_won=stdev([roll.result for roll in rolls])
    std_bet=stdev([roll.cost for roll in rolls])

    return Response(data={
        "total_spins":total_spins,
        "total_amoounth_won":total_amoounth_won,
        "max_amount_won":max_amount_won,
        "amount_won_per_spin":amount_won_per_spin,
        "std_won":std_won,
        "total_amount_bet":total_amount_bet,
        "max_amount_bet":max_amount_bet,
        "average_bet":average_bet,
        "std_bet":std_bet,
        "profit":profit,
    })

@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_roll(request,pk):
    roll = get_object_or_404(Roll, pk=pk)
    if  not roll.user == request.user:
        return Response({"error": "You don't have permission to see this roll"})
    serializer = RollSerializer(roll)
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_money(request):
    if float(request.data["amount"]) <= 0:
        return Response({"error": "Invalid amount"})
    request.user.balance += float(request.data["amount"])
    request.user.save()
    return Response({"success": "Successfully added money."})


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def spin_machine(request):
    if float(request.data["cost"]) > request.user.balance:
        return Response({"error": "Not enough money"})
    if float(request.data["cost"]) <= 0:
        return Response({"error": "Invalid bet"})

    slot_machine=Slot_machine()
    multyplier, roll_board, winning_lines=slot_machine.roll_machine()
    board_info={"roll_board":roll_board,"winning_lines":winning_lines}

    data = {
        'user':request.user.pk,
        'cost':request.data["cost"],
        'board_info':board_info,
        'winings_multyplier':multyplier,
    }
    serializer=RollSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        
        request.user.balance += float(request.data["cost"])*multyplier - float(request.data["cost"])
        request.user.save()
        return Response(serializer.data)
    return Response(serializer.errors)