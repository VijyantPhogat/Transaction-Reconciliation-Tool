
# Transaction Reconciliation Tool

### Overview

This Python tool automates the process of reconciling transactions between two PDF files. It matches transactions based on the Date, Debit, and Credit values and identifies unmatched transactions in each file.

The tool excludes transactions where both Debit and Credit are zero and generates an Excel file containing the unmatched transactions.

### Features

	•	Extracts transactions from PDF files with consistent formatting.
	•	Matches transactions by:
	•	Date
	•	Debit
	•	Credit
	•	Flags and outputs unmatched transactions.
	•	Skips rows with zero Debit and Credit values.
	•	Saves unmatched transactions to an Excel file for review.

### Prerequisites

	•	Python 3.x installed on your system.
	•	Required libraries:

pip install pymupdf pandas openpyxl

### Usage

	1.	Place the two PDF files in the same directory as the script.
	2.	Update the file names in the script if needed:

file1 = "ReconciledItemsReport.pdf"
file2 = "Search_20112024 - 2 Oct 2024.pdf"


	3.	Run the script:

python3 script_name.py


	4.	The output file Unmatched_Transactions_By_Date.xlsx will be saved in the same directory.

### Output

The output Excel file contains the following columns:
	•	Date: The transaction date.
	•	Description: A brief description of the transaction.
	•	Debit: The debit amount.
	•	Credit: The credit amount.
	•	Source: Indicates whether the transaction is unmatched in File 1 or File 2.

### Example

Date	Description	Debit	Credit	Source
02 Oct 2024	Deposit from ABC	500.00	0.00	File 1
02 Oct 2024	Rent payment by XYZ	0.00	700.00	File 2

### Known Limitations

	•	Assumes a structured PDF format with distinct rows for each transaction.
	•	Does not process scanned image PDFs. Use OCR tools (e.g., Tesseract) to convert images to text if needed.
