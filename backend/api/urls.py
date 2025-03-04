from django.urls import path
from .views import SkincareRecommendation

urlpatterns = [
    path('recommend/', SkincareRecommendation.as_view(), name="recommend"),
]
