from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ai.model import analyze_skin_problem  # AI Modelimizi içe aktar

class SkincareRecommendation(APIView):
    def post(self, request):
        user_input = request.data.get("problem", "").lower()
        # recommendations = analyze_skin_problem(user_input)  # AI Modelini çağır
        recommendations, ingredients, warning_message = analyze_skin_problem(user_input)  # AI Modelini çağır
        response_data = {
            "recommendations": recommendations,
            "ingredients": ingredients,  # İçecek önerilerini ekliyoruz
            "warning_message": warning_message  # Uyarı mesajını ekliyoruz
        }
        return Response(response_data, status=status.HTTP_200_OK)
        # return Response({"recommendations": recommendations}, status=status.HTTP_200_OK)

