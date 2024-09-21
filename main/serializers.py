from rest_framework import serializers
from .models import LLMUseCases, Conversation


class TTSSerializer(serializers.Serializer):
    """
    This serializer is used to get text which is used to process client request data
    """
    text = serializers.CharField()

    
class LLMUseCasesSerializer(serializers.ModelSerializer):
    """
    This serializer is used to retrieve data about LLMUseCases
    """
    class Meta:
        model = LLMUseCases
        fields = [
            "id", 
            "company_name",
            "industry_name",
            "function",
            "agent_role",
            "service",
            "issue",
            "language"
        ]
        
        
class ConversationCreateSerializer(serializers.ModelSerializer):
    """
    This serializer is used to create conversation
    """
    llm_use_case = serializers.UUIDField()
    customer = serializers.UUIDField(required=False, allow_null=True)
    
    class Meta:
        model = Conversation
        fields = [
            "id", 
            "llm_use_case", 
            "customer", 
        ]


class ConversationDetailSerializer(serializers.ModelSerializer):
    """
    This serializer is used to keep track of messages being sent in one conversation
    """
    
    class Meta:
        model = Conversation
        fields = ["id", "messages"]