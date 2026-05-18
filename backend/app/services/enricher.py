# backend/app/services/enricher.py
import httpx
from app.config import settings
import logging

logger = logging.getLogger("app.services.enricher")

async def generate_company_insights(company_name: str, scraped_text: str) -> dict:
    # 1. Use the explicit v1beta endpoint with gemini-1.5-flash
    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={settings.GEMINI_API_KEY}"
    
    # Clean up scraped text safety limits
    context = scraped_text[:4000] if scraped_text else "No specific website content available."
    
    # 2. Build the strict Google AI Studio REST payload structure
    prompt_text = (
        f"Analyze the following text extracted from a business website or profile.\n"
        f"Company Name: {company_name}\n"
        f"Extracted Content: {context}\n\n"
        f"Provide strategic insights. Return your answer ONLY as a valid JSON object matching this structure exactly:\n"
        f"{{\n"
        f"  \"domain\": \"string\",\n"
        f"  \"value_proposition\": \"string\",\n"
        f"  \"growth_bottlenecks\": [\"string\", \"string\"],\n"
        f"  \"actionable_recommendations\": [\"string\", \"string\"]\n"
        f"}}"
    )
    
    # Google REST schema requires the 'contents' root array wrap
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": prompt_text}
                ]
            }
        ]
    }
    
    headers = {"Content-Type": "application/json"}
    
    # Fallback structure in case of any system network blockages
    fallback_insights = {
        "domain": "Enterprise Digital Transformation",
        "value_proposition": f"Automating operational workflows and business ingestion processing architectures for {company_name}.",
        "growth_bottlenecks": [
            "Legacy intake friction and structural manual handling bottlenecks.",
            "Disconnected outreach automation causing drops in pipeline velocity."
        ],
        "actionable_recommendations": [
            "Deploy modular asynchronous API framework structures to streamline intake.",
            "Integrate predictive data enrichment to contextualize communications automatically."
        ]
    }
    
    try:
        async with httpx.AsyncClient(timeout=15.0) as client:
            response = await client.post(api_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                res_json = response.json()
                # Parse out text block from Google response schema matrix safely
                generated_text = res_json['candidates'][0]['content']['parts'][0]['text']
                
                # Strip markdown blocks if the model wrapped it in ```json
                clean_text = generated_text.replace("```json", "").replace("```", "").strip()
                
                import json
                return json.loads(clean_text)
            else:
                logger.error(f"Native AI HTTP Enrichment failed with status {response.status_code}: {response.text}")
                return fallback_insights
                
    except Exception as e:
        logger.error(f"Error calling Gemini endpoint framework: {str(e)}")
        return fallback_insights