from openai import OpenAI
from config import OPENAI_API_KEY

client = OpenAI(api_key=OPENAI_API_KEY)

def generate_brief(raw_text: str) -> str:
    prompt = f"""
Ты — профессиональный ассистент по сбору технических заданий.
Преврати неструктурированный клиентский запрос в чёткое ТЗ.

Структура:
- Название проекта
- Цель
- Основные задачи
- Целевая аудитория
- Требования (дизайн / функционал)
- Сроки
- Дополнительно (если есть)

Исходный текст:
\"\"\"
{raw_text}
\"\"\"
"""

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5,
        max_tokens=800
    )

    return response.choices[0].message.content.strip()
