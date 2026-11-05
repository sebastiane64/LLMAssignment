# Run this as a NEW Colab cell after Step 5 and before rerunning Step 6.
# Keeps SEC downloads; rebuilds model checkpoints under the stricter rules.
import re

QUALITY_RULES = """
Additional precision rules:
A heading, existing deployment, customer adoption, or demand statement alone is NOT a new announcement.
The evidence must explicitly say the named product was introduced, launched, released, debuted,
unveiled, made newly available, or began sampling. A sentence mentioning 'the launch of PRODUCT'
qualifies. Do not infer that every chip/component powering a newly available system is itself new.
Do not create separate rows for components merely mentioned alongside a release. A component qualifies
only when its own new release is explicit. Exclude generic platform/category headings.
Deduplicate brand-prefixed and unprefixed names for the same product. Use one consistent full name.
Descriptions must contain only facts supported by the evidence; do not add 'new' or OEM availability
unless the source states it.
"""
if QUALITY_RULES not in PROMPT:
    PROMPT += "\n" + QUALITY_RULES

# Save the original only once so rerunning this cell never stacks wrappers.
if "_original_extract_products" not in globals():
    _original_extract_products = extract_products

launch_language = re.compile(
    r"\b(introduc(?:e[ds]?|ing)|launch(?:ed|es|ing)?|releas(?:e[ds]?|ing)|"
    r"debut(?:ed|s|ing)?|unveil(?:ed|s|ing)?|now available|newly available|"
    r"began sampling|begin(?:s|ning)? sampling|announc(?:e[ds]?|ing))\b", re.I)

def product_identity(name, ticker):
    words = re.sub(r"[^\w\s]", " ", name.casefold()).split()
    brands = {ticker.casefold(), "amd", "nvidia", "intel", "apple", "microsoft",
              "amazon", "google", "alphabet", "meta", "tesla", "qualcomm"}
    while words and words[0] in brands:
        words.pop(0)
    return " ".join(words)

def extract_products(text, meta):
    rows, entities, rejected, usage = _original_extract_products(text, meta)
    unique = {}
    for row in rows:
        if not launch_language.search(row["evidence_quote"]):
            rejected.append({**row, "reason":"No explicit announcement language in evidence"})
            continue
        identity = product_identity(row["new_product"], meta["stock_name"])
        if identity in unique:
            rejected.append({**row, "reason":"Duplicate product alias in same filing"})
            continue
        unique[identity] = row
    return list(unique.values()), entities, rejected, usage

# Invalidate old extraction results, preserving cached downloads and API usage history.
# Only records for selected filings are moved; no files are deleted.
archive_dir = OUT / "before_quality_patch"
archive_dir.mkdir(exist_ok=True)
moved = 0
for meta in candidates:
    checkpoint = OUT / (meta["accession"] + ".json")
    if checkpoint.exists():
        destination = archive_dir / checkpoint.name
        if not destination.exists():
            checkpoint.rename(destination)
            moved += 1
print(f"Quality patch installed. Archived {moved} old checkpoints; SEC download cache retained.")
print("Run Step 6 with RUN_LIMIT = 5 again, then Step 7.")
