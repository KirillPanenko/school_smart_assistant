"""
Модуль для работы с языковой моделью GigaChat.
"""

from langchain.chat_models.gigachat import GigaChat
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.chat import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    MessagesPlaceholder,
)

from school_assistant.config.config import GIGACHAT_AUTH_TOKEN, SYSTEM_PROMPT


class AssistantLLM:
    """
    Класс для работы с языковой моделью GigaChat как школьного ассистента.
    """

    def __init__(self, auth_token=GIGACHAT_AUTH_TOKEN, system_prompt=SYSTEM_PROMPT):
        """
        Инициализирует экземпляр модели GigaChat с заданным системным промптом.

        Args:
            auth_token (str): Токен авторизации для GigaChat.
            system_prompt (str): Системный промпт для модели.
        """
        self.auth_token = auth_token
        self.system_prompt = system_prompt
        self.conversation = self._init_conversation()

    def _init_conversation(self):
        """
        Инициализирует цепочку разговора с LLM.

        Returns:
            ConversationChain: Объект цепочки разговора.
        """
        # Создаем шаблон чата с использованием системного сообщения, истории и сообщения пользователя
        chat_prompt = ChatPromptTemplate.from_messages(
            [
                SystemMessagePromptTemplate.from_template(self.system_prompt),
                MessagesPlaceholder(variable_name="history"),
                HumanMessagePromptTemplate.from_template("{input}"),
            ]
        )

        # Инициализация LLM
        llm = GigaChat(credentials=self.auth_token, verify_ssl_certs=False)

        # Создание цепочки разговора с кастомным промптом и корректной памятью
        return ConversationChain(
            llm=llm,
            prompt=chat_prompt,
            verbose=True,
            memory=ConversationBufferMemory(return_messages=True),
        )

    def get_response(self, user_input):
        """
        Получает ответ от модели на вопрос пользователя.

        Args:
            user_input (str): Вопрос или запрос пользователя.

        Returns:
            str: Ответ модели.
        """
        try:
            response = self.conversation.predict(input=user_input)
            return response
        except Exception as e:
            print(f"Ошибка при получении ответа от LLM: {str(e)}")
            return "Извините, произошла ошибка при обработке вашего запроса."
