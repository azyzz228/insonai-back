import json
import os
from django.db import transaction
from django.forms.models import model_to_dict
from django.http import FileResponse, Http404

from rest_framework import viewsets, status, views, generics
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from .serializers import (
    TTSSerializer,
    ConversationSerializer,
    LLMUseCasesSerializer,
)
from .models import (
    Conversation, 
    LLMUseCases,
    LLMUseCaseSetup
)

from main.ai.tts import speech_to_text
from main.ai.llm import client_speech_text_to_llm
from main.ai.stt import process_audio_and_send_request

class TTSView(views.APIView):
    serializer_class = TTSSerializer
    permission_classes = []
    authentication_classes = []

    def post(self, request, *args, **kwargs):
        conversation_id = self.kwargs.get("conversation_id")
        try:
            conversation = Conversation.objects.get(pk=conversation_id)
        except Conversation.DoesNotExist:
            raise Http404
        
        try:
            messages = json.loads(conversation.messages)
        except json.JSONDecodeError:
            raise ValidationError(f"Could not load json of messaged in conversation with id:{conversation_id}")
        
        print("[-] Starting STT")
        # add client speech to conversation messages, to keep messages history for LLM
        client_speech_text = request.data.get("text")
        messages.append({"role": "user", "content": client_speech_text})

        # trigger LLM service
        print("[-] SENDING TO LLM")
        llm_text = client_speech_text_to_llm(messages)
        messages.append({"role": "assistant", "content": llm_text})

        print("[+] LLM TEXT RESULT")
        print(llm_text)

        # Serialize the updated list back to a JSON string and update conversation
        conversation.messages = json.dumps(messages)
        conversation.save(update_fields=["messages"])

        
        # create audio from LLM service response text
        filepath = speech_to_text(llm_text)
        return FileResponse(
            open(filepath, "rb"), filename=os.path.basename(filepath), as_attachment=True
        )


class LLMUseCasesViewSet(viewsets.GenericViewSet):
    """
    ViewSet to serve get and list endpoints of LLMUseCases objects
    """
    
    queryset = LLMUseCases.objects.all()
    serializer_class = LLMUseCasesSerializer
    permission_classes = []
    authentication_classes = []
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ConversationCreateView(generics.GenericAPIView):
    """
    This endpoint is used to start a new conversation.
    It creates a conversation by including LLM use case data 
    and its setup data, both rendered into the conversation.
    """
    queryset = Conversation.objects.all()
    serializer_class = ConversationSerializer
    permission_classes = []
    authentication_classes = []

    @transaction.atomic
    def post(self, request, *args, **kwargs):
        # Validate the incoming request
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        
        # Get and validate the llm_use_case
        llm_use_case = self.get_llm_use_case(validated_data.pop("llm_use_case"))
        
        # Retrieve and populate the setup data
        setup_data = self.get_and_populate_setup_data(llm_use_case)

        # Create the conversation with setup and use case data
        conversation = self.create_conversation(validated_data, llm_use_case, setup_data)

        if not conversation:
            return Response({"ok": False}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"ok": True, "conversation_id": str(conversation.pk)}, status=status.HTTP_201_CREATED)
    
    def get_llm_use_case(self, llm_use_case_id):
        """
        Retrieves the LLM use case by ID and validates it.
        Raises a ValidationError if not found.
        """
        if not llm_use_case_id:
            raise ValidationError("The field 'llm_use_case' is required.")
        
        try:
            return LLMUseCases.objects.get(pk=llm_use_case_id)
        except LLMUseCases.DoesNotExist:
            raise ValidationError("The specified LLM use case does not exist.")
    
    def get_and_populate_setup_data(self, llm_use_case):
        """
        Retrieves the setup data associated with the LLM use case, 
        and populates missing placeholders with actual data from the use case.
        """
        try:
            setup_template = LLMUseCaseSetup.objects.get(llm_use_case=llm_use_case)
        except LLMUseCaseSetup.DoesNotExist:
            raise ValidationError("LLM use case setup data is missing.")

        return setup_template.setup_data

    def create_conversation(self, validated_data, llm_use_case, setup_data):
        """
        Creates the conversation with the populated setup data 
        and LLM use case data.
        """
        return Conversation.objects.create(
            llm_use_case=llm_use_case,
            messages=json.dumps(
                [
                    {"role": "system", "content": setup_data},
                ]
            ),
            **validated_data
        )
