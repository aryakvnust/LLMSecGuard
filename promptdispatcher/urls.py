from django.urls import path
from .views import CreatePrompt

urlpatterns = [
    path('createprompt/', CreatePrompt.as_view(), name='createprompt'),
]
