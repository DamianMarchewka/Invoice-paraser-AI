import pdfplumber
import statistics
import re


REPLACEMENTS = {
    "Data wystawienia": "Issue date",
    "Data sprzedaży": "Sale date",
    "Sprzedawca": "Seller",
    "Nabywca": "Buyer",
    "Razem": "Total",
    "NIP": "Tax ID",
    "Brutto": "Gross",
    "Netto": "Net",
    "VAT": "VAT",
    "Nazwa towaru": "Item",
    "Ilość": "Quantity",
    "Cena netto": "Net price",
    "Wartość brutto": "Gross value",
    "usługi": ""
}


NOISE_KEYWORDS = ["Strona", "Page", "www.", "tel.", "fax"]


def normalize_text(text: str) -> str:
    for pl, en in REPLACEMENTS.items():
        text = text.replace(pl, en)
    return text


def is_noise(line: str) -> bool:
    return any(k.lower() in line.lower() for k in NOISE_KEYWORDS)


def should_merge(prev_line: str, current_line: str) -> bool:
    if "|" in current_line:
        return False
    if len(current_line) < 40 and not re.search(r"[.:]$", prev_line):
        return True
    return False


def extract_numbers(text: str):
    return re.findall(r"\d+[.,]?\d*", text)


def clean_row_tail(line: str) -> str:
    """
    Usuwa tekst po kwocie (np. '5535.00 PLN Rozwój architektury')
    """
    match = re.search(r"(PLN)(.*)", line)
    if match:
        tail = match.group(2).strip()
        if tail and "|" not in tail:
            return line[:match.end(1)]
    return line


def enforce_line_breaks(text: str) -> str:
    """
    Rozdziela kluczowe pola na osobne linie
    """
    keywords = [
        "FAKTURA VAT",
        "Numer faktury:",
        "Issue date:",
        "Sale date:"
    ]

    for kw in keywords:
        text = text.replace(kw, f"\n{kw}")

    return text.strip()


def extractor_text(pdf_path: str) -> str:
    full_text = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            words = page.extract_words()
            if not words:
                continue

            words_sorted = sorted(words, key=lambda w: (w["top"], w["x0"]))

            heights = [w["bottom"] - w["top"] for w in words_sorted]
            median_height = statistics.median(heights) if heights else 10
            y_tolerance = median_height * 0.6

            lines = []
            current_line = []
            current_top = words_sorted[0]["top"]

            for word in words_sorted:
                if abs(word["top"] - current_top) <= y_tolerance:
                    current_line.append(word)
                else:
                    lines.append(current_line)
                    current_line = [word]
                    current_top = word["top"]

            if current_line:
                lines.append(current_line)

            raw_lines = []

            for line in lines:
                line = sorted(line, key=lambda w: w["x0"])
                line_str = ""
                last_x1 = None

                for word in line:
                    if last_x1 is not None:
                        gap = word["x0"] - last_x1

                        if gap > 15:
                            line_str += " | "
                        elif gap > 2:
                            line_str += " "

                    line_str += word["text"]
                    last_x1 = word["x1"]

                line_str = line_str.strip()

                if not line_str:
                    continue

                line_str = normalize_text(line_str)

                if is_noise(line_str):
                    continue

                raw_lines.append(line_str)

            merged_lines = []
            for line in raw_lines:
                if merged_lines and should_merge(merged_lines[-1], line):
                    merged_lines[-1] += " " + line
                else:
                    merged_lines.append(line)

            for line in merged_lines:

                if "Total" in line and "|" in line:
                    numbers = extract_numbers(line)

                    if len(numbers) >= 2:
                        net = numbers[0].replace(",", ".")
                        gross = numbers[1].replace(",", ".")

                        full_text.append(f"Total net: {net} PLN")
                        full_text.append(f"Total gross: {gross} PLN")
                        continue

                line = clean_row_tail(line)

                if " | " in line:
                    line = "[ROW] " + line

                full_text.append(line)

    result = "\n".join(full_text)
    result = enforce_line_breaks(result)

    return result