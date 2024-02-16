from rest_framework.response import Response
from machine.serializers import RollSerializer


def handle_spin_result(request, multiplier, roll_board, winning_lines, scater_multiplier, scater_positions):
    board_info = {"roll_board": roll_board,
                  "winning_lines": winning_lines,
                  "scater_positions": scater_positions}

    data = {
        'user': request.user.pk,
        'cost': request.data["cost"],
        'board_info': board_info,
        'winings_multiplier': multiplier,
        'scatter_multiplier': scater_multiplier,
    }
    serializer = RollSerializer(data=data)

    if serializer.is_valid():
        serializer.save()

        request.user.balance += float(request.data["cost"]) * \
            multiplier - float(request.data["cost"])
        request.user.save()
        return Response(serializer.data)
    return Response(serializer.errors)
