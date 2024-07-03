from groq import Groq

class LLMIntegration:
    def __init__(self, api_key):
        self.client = Groq(
            api_key=api_key,
        )
        self.model = "llama3-8b-8192"  # Substitua pelo modelo desejado

    def query_model(self, prompt):
        try:
            # Adicionando instrução para responder em português
            prompt_with_language = f"Por favor, responda em português.\n{prompt}"
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {
                        "role": "user",
                        "content": prompt_with_language,
                    }
                ],
                model=self.model,
            )
            return chat_completion.choices[0].message.content
        except Exception as e:
            return f"Erro na requisição: {e}"

llm_integration = LLMIntegration('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')
