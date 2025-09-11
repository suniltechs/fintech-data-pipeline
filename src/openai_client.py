from groq import Groq
import os

class OpenAIClient:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate_insights(self, symbol: str, data: dict):
        prompt = f"""
You are an AI financial analyst. Based on the following stock data for {symbol}:

{data}

Provide:
1. A brief summary of performance.
2. Two to three actionable recommendations.
"""
        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",  # updated to supported model
                messages=[
                    {"role": "system", "content": "You are a concise and clear financial AI assistant."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=500
            )
            content = response.choices[0].message.content.strip()
            parts = content.split("\n", 1)
            summary = parts[0]
            recommendations = parts[1] if len(parts) > 1 else "No recommendations."
            return summary, recommendations
        except Exception as e:
            print("Error generating insights with Groq:", e)
            return None, None
