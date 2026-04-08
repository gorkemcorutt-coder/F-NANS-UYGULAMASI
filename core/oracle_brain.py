import google.generativeai as genai
from google.generativeai import types
from config import settings
from .system_prompt import ORACLE_SYSTEM_PROMPT

class OracleBrain:
    def __init__(self):
        # Configure the genai library with the API key from settings
        if settings.gemini_api_key:
            genai.configure(api_key=settings.gemini_api_key)
        else:
            print("WARNING: Gemini API Key is missing. Brain cannot function properly without it.")

        # Optionally use tools like google_search if available in the SDK
        # We will wrap it in a try-except to avoid issues if the SDK version differs
        tools = []
        try:
            tools.append(types.Tool(google_search=types.GoogleSearch()))
        except AttributeError:
            pass # fallback if GoogleSearch tool is not in this version of the SDK

        # Configuration specified in the architecture document
        generation_config = genai.GenerationConfig(
            temperature=0.25,
            top_p=0.85,
            top_k=40,
            max_output_tokens=8192,
        )

        # We use gemini-1.5-flash to ensure compatibility and speed
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            system_instruction=ORACLE_SYSTEM_PROMPT,
            tools=tools if tools else None,
            generation_config=generation_config,
        )

    def generate_daily_report(self, market_data: dict) -> str:
        """
        Generates the daily intelligence report using current market data.
        """
        prompt = f"""
        Kullanıcı `/gunluk` komutunu çalıştırdı.
        Lütfen güncel verileri kullanarak GÜNLÜK İSTİHBARAT raporunu hazırla.
        
        Sana sağlanan güncel piyasa verileri:
        {market_data}
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Hata: AI modeli ile iletişim kurulamadı. Detay: {str(e)}"

# Singleton benzeri bir obje yapalım
brain = OracleBrain()
