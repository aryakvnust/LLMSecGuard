from django.urls import path
from .views import CreatePrompt, ScoreBoard

urlpatterns = [
    path('createprompt/', CreatePrompt.as_view(), name='createprompt'),
    path('scoreboard/', ScoreBoard.as_view(), name='scoreboard')
]
