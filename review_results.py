"""Reproduce evidence-based review. Usage: python review_results.py INPUT_ZIP OUTPUT_DIR"""
import csv,io,json,sys,zipfile,hashlib
from pathlib import Path
source=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True)
z=zipfile.ZipFile(source)
evidence_bytes=z.read("evidence.csv")
EXPECTED_0fe4a6c41f2d87a1a42cd0c6681933ba2d05ce49324ffca55641c7161b51f626 = "0fe4a6c41f2d87a1a42cd0c6681933ba2d05ce49324ffca55641c7161b51f626"
if hashlib.sha256(evidence_bytes).hexdigest()!=EXPECTED_0fe4a6c41f2d87a1a42cd0c6681933ba2d05ce49324ffca55641c7161b51f626:
    raise ValueError("These review decisions apply only to the reviewed 99-filing run. Review changed data separately.")
rows=list(csv.DictReader(io.StringIO(evidence_bytes.decode())))
with Path(__file__).with_name("review_decisions.csv").open() as f:
    decisions=list(csv.DictReader(f))
retained=[];reviewed=[]
for row,decision in zip(rows,decisions):
    assert row["accession"]==decision["accession"] and row["new_product"]==decision["new_product"]
    reviewed.append({**row,**decision})
    if decision["decision"]=="retain":
        if decision["revised_description"]:row["product_description"]=decision["revised_description"]
        retained.append(row)
assert len(rows)==len(decisions)
columns=["company_name","stock_name","filing_time","new_product","product_description"]
assert all(len(r["product_description"])<180 for r in retained)
def save(name,data,fields,delimiter=","):
    with (out/name).open("w",newline="",encoding="utf-8") as f:
        w=csv.DictWriter(f,fieldnames=fields,extrasaction="ignore",delimiter=delimiter)
        w.writeheader();w.writerows(data)
save("products.csv",retained,columns)
save("products_pipe.txt",retained,columns,"|")
save("evidence_reviewed.csv",retained,list(rows[0]))
save("review_log.csv",reviewed,list(reviewed[0]))
for name in ("filing_audit.csv","named_entities.csv","errors.jsonl"):
    if name in z.namelist():(out/name).write_bytes(z.read(name))
summary=json.loads(z.read("run_summary.json"))
summary.update(raw_candidate_rows=len(rows),reviewed_product_rows=len(retained),
    excluded_in_review=len(rows)-len(retained),reviewed_filings_with_products=len(set(r["accession"] for r in retained)),
    review_basis="Supplied evidence quotes; source pages were not independently re-downloaded during review.",
    failed_filing="0001628280-26-063820 (TSLA): ValidationError")
(out/"run_summary_reviewed.json").write_text(json.dumps(summary,indent=2))
print(json.dumps(summary,indent=2))
