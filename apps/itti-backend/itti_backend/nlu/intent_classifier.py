"""Intent classifier for the VuelaConNosotros chatbot."""

from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from ..core.config import settings


class IntentClassifier:
    """Classifies the user's intent based on their message."""

    def __init__(self):
        """Initializes the IntentClassifier."""
        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            google_api_key=settings.GEMINI_API_KEY,
            temperature=0,
        )
        self.prompt = self._build_prompt()

    def _build_prompt(self) -> ChatPromptTemplate:
        """Builds the prompt for intent classification with few-shot examples."""
        system_message = """
            Eres un clasificador de intenciones. Tu única tarea es clasificar el texto del usuario en una de las siguientes categorías:
            - consultar_estado_vuelo
            - cambiar_vuelo
            - saludo
            - despedida
            - agradecimiento
            - desconocida

            Responde únicamente con el nombre de la categoría. No agregues explicaciones ni texto adicional.

            Ejemplos:
            - Usuario: "Hola, ¿cómo estás?" -> saludo
            - Usuario: "Quisiera saber cómo viene el vuelo VW123" -> consultar_estado_vuelo
            - Usuario: "Necesito cambiar mi pasaje a Madrid" -> cambiar_vuelo
            - Usuario: "Adiós, que tengas un buen día" -> despedida
            - Usuario: "Muchas gracias por tu ayuda" -> agradecimiento
            - Usuario: "¿Cuál es la capital de Mongolia?" -> desconocida
            """
        return ChatPromptTemplate.from_messages(
            [
                ("system", system_message),
                ("human", "{text}"),
            ]
        )

    def classify(self, text: str) -> str:
        """Classifies the intent of the input text.

        Args:
            text: The user's message.

        Returns:
            The classified intent as a string.
        """
        chain = self.prompt | self.llm
        try:
            result = chain.invoke({"text": text})
            return result.content.strip()
        except Exception as e:
            print(f"Error during intent classification: {e}")
            return "desconocida"
