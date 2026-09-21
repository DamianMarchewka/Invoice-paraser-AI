# 📄 Invoice Parser (MVP)

Automatic extraction of structured data from invoice PDFs into JSON using Python and an LLM.

This project is a Proof-of-Concept tool designed for small accounting offices to reduce manual data entry from invoices.

---

## Important !!

for demo/testing only
not for production data

---

## 🚀 Features (MVP v0.1)

* 📥 Load invoice PDFs (text-based, no OCR)
* 🔍 Extract text using `pdfplumber`
* 🧹 Clean and structure text for LLM processing
* 🤖 Extract invoice data via LLM
* 📦 Output structured JSON
* ✅ Validate data using Pydantic

---

## 🧱 Project Structure

```
invoice_parser/
│
├── app/
│   ├── extractor.py   # PDF → text (clean + structured)
│   ├── parser.py      # LLM → JSON
│   ├── schemas.py     # Data validation (Pydantic)
│   └── main.py        # CLI entrypoint
│
├── data/              # Sample invoice PDFs
├── tests/             # Tests (optional)
└── requirements.txt
```

---

## ⚙️ Installation

### 1. Clone repository

```
git clone https://github.com/your-username/invoice-parser.git
cd invoice-parser
```

### 2. Create virtual environment

```
python -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```
pip install -r requirements.txt
```

---

## 🔑 API Configuration

Set your API key as an environment variable:

```
export OPENAI_API_KEY="your_api_key"
```

Or persist it:

```
echo 'export OPENAI_API_KEY="your_api_key"' >> ~/.zshrc
source ~/.zshrc
```

---

## ▶️ Usage

```bash id="run1"
python app/main.py data/sample_invoice.pdf
```

---

## 📤 Example Output

```
{
  "invoice_number": "FV/2026/09/104",
  "issue_date": "2026-09-12",
  "seller_name": "TechSol Sp. z o.o.",
  "seller_tax_id": "5250001234",
  "buyer_name": "PPHU Omega Sp. k.",
  "buyer_tax_id": "7251998877",
  "net_amount": 7300.0,
  "tax_amount": 1679.0,
  "gross_amount": 8979.0,
  "currency": "PLN"
}
```

---

## 🔄 Processing Pipeline

```
PDF
 ↓
Text extraction (pdfplumber)
 ↓
Text cleaning & structuring
 ↓
LLM (data extraction)
 ↓
Validation (Pydantic)
 ↓
JSON output
```

---

## 🧠 Design Principles

* CLI-only (no UI)
* No database
* No external integrations
* Focus on working end-to-end MVP
* Iterative improvement based on real outputs

---

## ⚠️ Limitations

* Only text-based PDFs (no OCR support yet)
* No multi-language support
* Limited table understanding
* Dependent on LLM output quality

---

## 🛠️ Tech Stack

* Python 3.11+
* pdfplumber
* OpenAI API
* Pydantic

---

## 📈 Roadmap

* [ ] Retry logic for LLM (auto-fix invalid JSON)
* [ ] Improved validation (dates, tax IDs)
* [ ] Batch processing (multiple invoices)
* [ ] Error logging
* [ ] OCR support (for scanned PDFs)
* [ ] API layer (FastAPI)

---

## 💡 Project Goal

To build a simple, scalable document processing pipeline (PDF → structured data) that can evolve into:

* accounting automation tools
* ERP integrations
* general business document processing systems

---
