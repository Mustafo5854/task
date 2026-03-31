from django.urls import path
from .views import TopLanguagesByYearView

urlpatterns = [
    path('top-languages/', TopLanguagesByYearView.as_view()),
]