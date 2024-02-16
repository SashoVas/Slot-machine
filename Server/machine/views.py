from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from machine.models import User, Roll
from machine.serializers import UserSerializer, RollSerializer
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from machine import slot_machine_settings
from machine.slot_machine import Slot_machine
from statistics import stdev
from django.db.models import Sum, Avg, Max
from machine.decorators import roll_decorator
from machine.utils import handle_spin_result
import json
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
        return Response({"error": "Wrong password"}, status=400)
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
    return Response(serializer.errors, status=400)


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
    total_amoounth_won = sum([roll.result for roll in rolls])
    total_amount_bet = sum([roll.cost for roll in rolls])

    return Response(data={
        "total_spins": len(rolls),
        "total_amoounth_won": total_amoounth_won,
        "max_amount_won": max([roll.result for roll in rolls]),
        "amount_won_per_spin": total_amoounth_won/len(rolls),
        "std_won": stdev([roll.result for roll in rolls]),
        "total_amount_bet": total_amount_bet,
        "max_amount_bet": max([roll.cost for roll in rolls]),
        "average_bet": total_amount_bet/len(rolls),
        "std_bet": stdev([roll.cost for roll in rolls]),
        "profit": total_amoounth_won-total_amount_bet,
        "max_multiplyer": max([roll.winings_multiplier for roll in rolls]),
        "average_multiplyer": sum(
            [roll.winings_multiplier for roll in rolls])/len(rolls),
        "std_multiplyer": stdev([roll.winings_multiplier for roll in rolls]),
    })


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_user_roll(request, pk):
    roll = get_object_or_404(Roll, pk=pk)
    if not roll.user == request.user:
        return Response({"error": "You don't have permission to see this roll"}, status=400)
    serializer = RollSerializer(roll)
    return Response(serializer.data)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def add_money(request):
    if float(request.data["amount"]) <= 0:
        return Response({"error": "Invalid amount"}, status=400)
    request.user.balance += float(request.data["amount"])
    request.user.save()
    return Response({"balance": request.user.balance})


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@roll_decorator
def spin_machine(request):

    slot_machine = Slot_machine()
    multiplier, roll_board, winning_lines, scater_multiplier, scater_positions = slot_machine.roll_machine()

    return handle_spin_result(request, multiplier, roll_board, winning_lines, scater_multiplier, scater_positions)


@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
@roll_decorator
def spin_machine_rigged(request):
    if request.data['password'] != slot_machine_settings.RIGGED_SPIN_PASSWORD:
        return Response({"error": "Wrong password"}, status=400)

    rigged_input = json.loads(request.data['rigged_reels_symbols'])

    slot_machine = Slot_machine(
        is_rigged=True, rigged_reels_symbols=rigged_input)

    multiplier, roll_board, winning_lines, scater_multiplier, scater_positions = slot_machine.roll_machine()
    return handle_spin_result(request, multiplier, roll_board, winning_lines, scater_multiplier, scater_positions)


@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_leaderboard(request, criteria):
    if criteria not in ["profit", "max_multyplyer", "amounth_bet", "amounth_won"]:
        return Response({"error": "Invalid criteria"}, status=400)
    rolls = (Roll.objects.prefetch_related('user')
             .values("user__username")
             .annotate(
        profit=Sum("winings_multiplier")*Avg("cost")-Sum("cost"),
        max_multyplyer=Max("winings_multiplier"),
        amounth_bet=Sum("cost"),
        amounth_won=Sum("winings_multiplier")*Avg("cost")
    ).order_by(f"-{criteria}"))[:10]

    return Response(rolls)
