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

## Implementation
The notebook runs in Google Colab with dependencies, private API configuration, SEC retrieval, sample selection, prompted NER, structured extraction, filing processing, and export. The default scope is 100 filings. Credentials are entered through a hidden runtime prompt; a contact email identifies SEC requests. Quality checks are integrated directly into extraction. Successful filing checkpoints and cached downloads support resuming interrupted runs.

HTML/text EX-99 exhibits are included; PDF exhibits are excluded. Description length is strictly below 180 characters. Evidence checks are followed by a separate, reproducible review of the recorded run.

## Reproduce the reviewed output
Download the raw_results.zip provided in the submission bundle, then run:

```sh
python review_results.py raw_results.zip results
```

The review script and review_decisions.csv apply only to the exact reviewed run. A hash check prevents accidental use on changed data. New runs require a fresh review. Repeat product announcements across separate filings remain separate records.

The notebook contains no embedded credentials or fabricated cell outputs. Recorded run artifacts provide the execution record. The methodology report documents scope, review criteria, and limitations.
