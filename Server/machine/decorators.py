from rest_framework.response import Response


def roll_decorator(func):

    def roll_validator(request):
        if float(request.data["cost"]) > request.user.balance:
            return Response({"error": "Not enough money"}, status=400)
        if float(request.data["cost"]) <= 0:
            return Response({"error": "Invalid bet"}, status=400)
        return func(request)
    return roll_validator
