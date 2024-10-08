import uuid
from django.db import models

        
class BaseModel(models.Model):
    """
    Base model is used to define common fields, which is id and timestamps
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_at = models.DateTimeField(auto_now=True)    

    class Meta:
        abstract = True
    
    
class Customer(BaseModel):
    """
    This model is used to collect breif data about customers
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=50)

        
class LLMUseCases(BaseModel):
    """
    This model is used to determine use cases of companies they are planning to fill information LLM
    """
    company_name = models.CharField(max_length=50)
    industry_name = models.CharField(max_length=50)
    function = models.CharField(max_length=50)
    agent_role = models.CharField(max_length=50)
    service = models.CharField(max_length=50)
    issue = models.CharField(max_length=50)
    task = models.CharField(max_length=255)
    language = models.CharField(max_length=50)


class LLMUseCaseSetup(BaseModel):
    """
    This model is used to get needed information from uses cases and process to LLM
    """
    llm_use_case = models.OneToOneField(
        to=LLMUseCases, 
        on_delete=models.CASCADE, 
        related_name="setup"
    )
    setup_data = models.JSONField()


class Conversation(BaseModel):
    """
    This model is used to create conversation between customer and LLM
    """
    llm_use_case = models.ForeignKey(
        to=LLMUseCases,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    customer = models.ForeignKey(
        to=Customer,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    messages = models.TextField()
    # if use case was deleted, we save its name for future reference
    use_case_name = models.CharField(max_length=50, blank=True, null=True)
    # if customer was deleted, we save its phone and customer phone
    customer_name = models.CharField(max_length=50, blank=True, null=True)
    customer_phone = models.CharField(max_length=20, blank=True, null=True)