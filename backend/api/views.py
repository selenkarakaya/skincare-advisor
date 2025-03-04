# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from ai.model import analyze_skin_problem  # AI Modelimizi içe aktar

# class SkincareRecommendation(APIView):
#     def post(self, request):
#         user_input = request.data.get("problem", "").lower()
#         # recommendations = analyze_skin_problem(user_input)  # AI Modelini çağır
#         recommendations, ingredients, avoid, warning_message = analyze_skin_problem(user_input)  # AI Modelini çağır
#         response_data = {
#             "recommendations": recommendations,
#             "ingredients": ingredients,  # İçecek önerilerini ekliyoruz
#             "avoid":avoid,
#             "warning_message": warning_message  # Uyarı mesajını ekliyoruz
#         }
#         return Response(response_data, status=status.HTTP_200_OK)
#         # return Response({"recommendations": recommendations}, status=status.HTTP_200_OK)







            

import openai
from django.conf import settings
from rest_framework.decorators import api_view
from rest_framework.response import Response

# OpenAI API anahtarını ayarladık
openai.api_key = settings.OPENAI_API_KEY

@api_view(['POST'])
def get_skincare_advice(request):
    try:
        # Kullanıcıdan gelen problemi alıyoruz
        problem = request.data.get("problem", "")
        
        if not problem:
            return Response({"error": "Problem description is required!"}, status=400)
        
        # OpenAI API'ye istek yapıyoruz
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Kullanmak istediğiniz model
            messages=[
                {"role": "system", "content": "You are a skincare expert assistant."},
                {"role": "user", "content": problem}
            ]
        )

        # Cevabı alıyoruz ve uygun şekilde döndürüyoruz
        advice = response['choices'][0]['message']['content']
        return Response({"advice": advice})

    except Exception as e:
        return Response({"error": f"Server error: {str(e)}"}, status=500)
