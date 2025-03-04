# from django.urls import path
# from .views import SkincareRecommendation

# urlpatterns = [
#     path('recommend/', SkincareRecommendation.as_view(), name="recommend"),
    
# ]

from django.urls import path
from .views import get_skincare_advice

urlpatterns = [
    path('get_advice/', get_skincare_advice, name='get_advice'),
]

