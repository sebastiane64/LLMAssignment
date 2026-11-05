# SEC 8-K Product Announcement Extraction

Sebastian Esteban

[Open notebook in Google Colab](https://colab.research.google.com/github/sebastiane64/LLMAssignment/blob/main/SEC_8K_Colab.ipynb)

## Submitted results
100 filings selected, 99 successfully processed; one Tesla filing failed validation. The raw LLM run generated 80 candidate rows; evidence-based review excluded 18 and retained **62 product records across 13 filings**. This is an assisted review of supplied quotes, not an independent verification of all source pages or an accuracy benchmark.

- [Final five-column CSV](results/products.csv)
- [Methodology report](Methodology_Report.md)
- [Evidence with source links](results/evidence_reviewed.csv)
- [Review log](results/review_log.csv)
- [Run summary](results/run_summary_reviewed.json)

## Run in Colab
Run cells in order. Step 2 requests a private API key through a hidden prompt and a contact email for the SEC User-Agent. The key must never be hardcoded or committed. Start with five filings; inspect results, then set RUN_LIMIT=100 and rerun the processing/export cells. Downloads and successful extractions are cached. The integrated quality rules run before Step 6; the standalone quality_patch.py is retained for the original working-session workflow.

The notebook uses SEC submissions JSON metadata, BeautifulSoup parsing of primary filings and HTML/text EX-99 exhibits, prompted ORGANIZATION/PRODUCT named entity recognition, structured LLM outputs, quote checks, and a strict description length below 180 characters. PDF exhibits are excluded. Do not rerun quality_patch.py on an existing result folder unless intentionally archiving its checkpoints.

## Reproduce the reviewed output
Download the raw_results.zip provided in the submission bundle, then run:

```sh
python review_results.py raw_results.zip results
```

The review script and review_decisions.csv apply only to the exact reviewed run. A hash check prevents accidental use on changed data. New runs require a fresh review. Repeat product announcements across separate filings remain separate records.

The submitted source notebook has no embedded credentials and no invented execution outputs. The student's run artifacts provide the execution record. See the report for complete limitations. Add this repository URL to the top of your CV, as required by the assignment.
