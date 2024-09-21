from django.core.management.base import BaseCommand
from main.models import LLMUseCases, LLMUseCaseSetup


class Command(BaseCommand):
    help = 'Insert LLM use cases and their setups into the database'

    def handle(self, *args, **kwargs):
        # Define your data for LLM use cases
        use_case_data = [
            {
                "companyName": "HealthCo",
                "industryName": "healthcare",
                "function": "quality_assurance",
                "agentRole": "Customer Service Quality Assurance agent",
                "service": "patient feedback collection",
                "issue": "treatment for a throat infection",
                "task": "The LLM will initiate a conversation with the customer, ask about and rate their satisfaction, gathering information based on responses.",
                "language": "Uzbek"
            },
            {
                "companyName": "EduConsult",
                "industryName": "education",
                "function": "leads_processing",
                "agentRole": "Education Consultant",
                "service": "consultation",
                "issue": "overseas study programs",
                "task": "The LLM will initiate a conversation with the customer, ask about and rate their satisfaction, gathering information based on responses.",
                "language": "Uzbek"
            }
        ]

        # Insert data into the database
        for item in use_case_data:
            # Create the LLMUseCase
            llm_use_case = LLMUseCases.objects.create(
                company_name=item["companyName"],
                industry_name=item["industryName"],
                function=item["function"],
                agent_role=item["agentRole"],
                service=item["service"],
                task=item["task"],
                issue=item["issue"],
                language=item["language"]
            )

            # Render the setup data using the template and the current use case data
            setup_data = f"""
            The LLM acts as a {llm_use_case.agent_role} for a {llm_use_case.company_name} company in
            {llm_use_case.industry_name} industry in Uzbekistan. {llm_use_case.task} Text-based dialogue simulating phone interactions.
            The LLM will structure questions in {llm_use_case.language} only unless customer speaks in another language.
            Ask concise, open-ended questions relevant to {llm_use_case.service}. Limit each question to 2-3 sentences. 
            Based on the responses, guide the conversation naturally. Do greeting, ask the relevant first question,
            and wait for the response so that you can follow-up in {llm_use_case.language} language.
            """

            # Create the LLMUseCaseSetup
            LLMUseCaseSetup.objects.create(
                llm_use_case=llm_use_case,
                setup_data=setup_data
            )

        self.stdout.write(self.style.SUCCESS('LLM Use cases and their setups inserted successfully!'))
