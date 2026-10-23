import json
import re
from google import genai
from google.genai import types
from app.config import settings

def _fallback_items(raw_items: list) -> list:
    clean_items = []
    for item in raw_items[:3]:
        summary_clean = re.sub(r'<[^>]+>', '', item.get("summary", ""))
        clean_items.append({
            "title": item.get("title", ""),
            "summary": (summary_clean[:180] + "...") if len(summary_clean) > 180 else summary_clean,
            "source_name": item.get("source", ""),
            "source_url": item.get("link", "")
        })
    return clean_items

def summarize_category_news(category_label: str, raw_items: list) -> list:
    """Usa o Gemini 1.5 Flash para selecionar e sintetizar rigorosamente de 2 a 3 notícias."""
    if not settings.GEMINI_API_KEY:
        print("GEMINI_API_KEY não configurada. Usando fallback bruto.")
        return _fallback_items(raw_items)

    prompt = f"""
Você é o editor-chefe do aplicativo 'BREVE.', um resumo matinal diário de notícias altamente conciso, confiável e anti-fake news.

Categoria analisada: {category_label.upper()}
Notícias brutas coletadas:
{json.dumps(raw_items, ensure_ascii=False, indent=2)}

Sua tarefa:
1. Escolha estritamente de 2 a no máximo 3 notícias mais relevantes e factuais.
2. Elimine qualquer rumor, especulação sensacionalista ou redundâncias.
3. Para cada uma das escolhidas:
   - "title": Reescreva o título com clareza editorial (máx 80 caracteres).
   - "summary": Crie um resumo denso de 2 ou 3 frases pontuando o fato, contexto e impacto principal.
   - "source_name": Mantenha a fonte original.
   - "source_url": Mantenha o link correspondente.

Retorne SOMENTE uma lista em formato JSON válido contendo os objetos. Exemplo:
[
  {{
    "title": "...",
    "summary": "...",
    "source_name": "...",
    "source_url": "..."
  }}
]
"""
    client = genai.Client(api_key=settings.GEMINI_API_KEY)
    models_to_try = ["gemini-2.5-flash", "gemini-2.5-flash-lite"]

    for model_name in models_to_try:
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )

            raw_text = response.text.strip()
            if raw_text.startswith("```"):
                raw_text = re.sub(r"^```[a-zA-Z]*\n?", "", raw_text)
                raw_text = re.sub(r"\n?```$", "", raw_text)

            data = json.loads(raw_text)
            if isinstance(data, list) and len(data) > 0:
                return data[:3]
        except Exception as err:
            print(f"Tentativa com {model_name} para {category_label} falhou: {err}")
            continue

    print(f"Todas as tentativas de IA falharam para {category_label}. Usando fallback das notícias brutas.")
    return _fallback_items(raw_items)
