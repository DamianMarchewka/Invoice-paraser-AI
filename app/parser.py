from openai import OpenAI
import json

client = OpenAI()


def parse_invoice(text: str) -> dict:
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0,
        messages=[
            {
                "role": "system",
                "content": "Return ONLY valid JSON invoice data."
            },
            {
                "role": "user",
                "content": f"""
Extract invoice data from text.

Return JSON with fields:
invoice_number, issue_date, seller_name, seller_tax_id,
buyer_name, buyer_tax_id, net_amount, tax_amount, gross_amount, currency

Rules:
- no guessing
- null if missing
- dates YYYY-MM-DD
- numbers as float

TEXT:
{text}
"""
            }
        ]
    )

    return json.loads(response.choices[0].message.content)