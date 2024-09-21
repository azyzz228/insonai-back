from django.urls import path
from rest_framework.routers import DefaultRouter

from main.views import (
    TTSView,
    LLMUseCasesViewSet,
    ConversationCreateView,
    ConversationDetailView
)


app_name = "main"


router = DefaultRouter()
router.register("llm_use_cases", LLMUseCasesViewSet, basename="llm_use_cases")

urlpatterns = [
    path("create_conversation/", ConversationCreateView.as_view(), name="create_conversation"),
    path("create_conversation/<uuid:pk>/", ConversationDetailView.as_view(), name="detail_conversation"),
    path("client_speech_text/<uuid:conversation_id>/", TTSView.as_view(), name="client_speech_text"),
]

urlpatterns += router.urls