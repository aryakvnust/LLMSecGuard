from django.urls import path
from .views import CreatePrompt, ScoreBoard, LLMList, LLMDetails

urlpatterns = [
    path('createprompt/', CreatePrompt.as_view(), name='createprompt'),
    path('scoreboard/', ScoreBoard.as_view(), name='scoreboard'),
    path('models/', LLMList.as_view(), name='models'),
    path('models/<str:llm_type>', LLMDetails.as_view(), name='models')
]
