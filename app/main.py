import os
import sys
import json

try:
    from extractor import extractor_text
    from parser import parse_invoice
    from schemas import Invoice
except ImportError:
    print("Error: Could not import modules.")
    print("Make sure extractor.py, parser.py, schemas.py are available.")
    sys.exit(1)


def download_path() -> str:
    if len(sys.argv) < 2:
        print("Error: No path provided as a program argument!")
        print("Usage: python main.py <path_to_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    if not os.path.exists(pdf_path):
        print(f"Error: The path '{pdf_path}' does not exist.")
        sys.exit(1)

    print("Path loaded successfully.")
    return pdf_path


if __name__ == "__main__":
    user_path = download_path()

    # 1. Extract text
    extracted_text = extractor_text(user_path)

    print("\n--- Extracted text ---")
    print(extracted_text)

    # 2. LLM parsing
    try:
        raw_json = parse_invoice(extracted_text)
    except Exception as e:
        print("\n[ERROR] LLM parsing failed:", str(e))
        sys.exit(1)

    # 3. Validation (Pydantic)
    try:
        invoice = Invoice(**raw_json)
    except Exception as e:
        print("\n[ERROR] Schema validation failed:")
        print(raw_json)
        print(str(e))
        sys.exit(1)

    # 4. Output
    print("\n--- Parsed JSON ---")
    print(json.dumps(invoice.model_dump(), indent=2, ensure_ascii=False))