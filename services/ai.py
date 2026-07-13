import os
import json

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def generate_learning_roadmap(resources):

    prompt = """
You are an expert learning mentor.

The user has saved learning resources.

Group them into topics.

Then generate a recommended learning roadmap.

Return ONLY valid JSON. Do NOT return anything else. ONLY VALID JSON.

Example:

{
  "clusters":[
    {
      "topic":"Machine Learning",
      "resources":[
        "Attention Is All You Need"
      ]
    }
  ],
  "roadmap":[
    "Start with...",
    "Then learn...",
    "Finally..."
  ]
}

Resources:

"""

    for resource in resources:

        prompt += f"""

Title: {resource.get("title")}

Type: {resource.get("type")}

Description: {(resource.get("description") or "")[:250]}

"""

    response = client.models.generate_content(

        model="gemini-2.5-flash",

        contents=prompt

    )

    text = response.text

    text = text.replace("```json", "")

    text = text.replace("```", "")

    return json.loads(text)