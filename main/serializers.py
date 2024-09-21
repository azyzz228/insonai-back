from rest_framework import serializers
from .models import LLMUseCases, Conversation


class TTSSerializer(serializers.Serializer):
    text = serializers.CharField()

    
class LLMUseCasesSerializer(serializers.ModelSerializer):
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
        
        
class ConversationSerializer(serializers.ModelSerializer):
    llm_use_case = serializers.UUIDField()
    customer = serializers.UUIDField(required=False, allow_null=True)
    
    class Meta:
        model = Conversation
        fields = [
            "id", 
            "llm_use_case", 
            "customer", 
        ]
