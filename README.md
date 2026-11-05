# SEC 8-K Product Announcement Extraction

[Open in Google Colab](https://colab.research.google.com/github/sebastiane64/LLMAssignment/blob/main/SEC_8K_Colab.ipynb)

Run the notebook in order. Step 2 asks for an OpenAI API key through a hidden getpass input; never hardcode or commit it. API billing must be enabled separately. Enter a contact email for the SEC User-Agent.

Start with five filings, inspect the evidence, then set RUN_LIMIT=100 and rerun Steps 6–8. Ten recent filings are selected per company across ten technology/automotive companies. The code uses SEC submissions JSON and BeautifulSoup, including EX-99 HTML/text exhibits. Explicit LLM-based ORGANIZATION/PRODUCT NER and announcement extraction use structured outputs. One row per verified product per filing is exported; filings without verified announcements remain in the audit file. Descriptions are strictly fewer than 180 characters. Successful filings are checkpointed.

Outputs: products.csv (five required columns), products_pipe.txt, evidence.csv, named_entities.csv, filing_audit.csv, run_summary.json, JSON checkpoints, and an optional error log. Failed filings are not counted as successful negatives. Download the ZIP before the Colab session ends. The notebook has not yet been run with the student's API credentials; actual results must come from execution.

Limitations: purposive sample, possible SEC cloud-IP blocks, HTML/text exhibits only (PDF exhibits excluded), possible model errors and missed cross-chunk context. Exact quote checks support auditing but do not prove semantic correctness. Manually review source links and quotes. Product descriptions may be shortened to enforce the length limit. Repeated product announcements in different filings remain separate rows.

The methodology report should use the actual run summary, describe manual validation honestly, and include this repository URL. Add the URL at the top of your CV as required by the assignment.

Sources: https://www.sec.gov/search-filings/edgar-application-programming-interfaces and https://developers.openai.com/api/docs/guides/structured-outputs
