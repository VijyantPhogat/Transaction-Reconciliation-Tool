import fitz  # PyMuPDF for PDF processing
import pandas as pd

def extract_transactions_from_pdf(pdf_path):
    """
    Extracts transaction data from a PDF file.
    Filters out transactions where both Debit and Credit are zero.
    """
    doc = fitz.open(pdf_path)
    transactions = []
    
    for page in doc:
        text = page.get_text("text")
        lines = text.split("\n")
        
        for line in lines:
            parts = line.split()
            try:
                # Parse line based on assumed structure: Date, Description, Debit, Credit
                if len(parts) >= 4:
                    date = parts[0]
                    description = " ".join(parts[1:-2])  # Description in the middle
                    debit_credit = parts[-2:]
                    
                    debit = float(debit_credit[0].replace("$", "").replace(",", "")) if "$" in debit_credit[0] else 0.0
                    credit = float(debit_credit[1].replace("$", "").replace(",", "")) if "$" in debit_credit[1] else 0.0

                    # Exclude transactions where both Debit and Credit are zero
                    if not (debit == 0.0 and credit == 0.0):
                        transactions.append([date, description, debit, credit])
            except Exception as e:
                # Skip malformed lines
                continue

    doc.close()
    return pd.DataFrame(transactions, columns=["Date", "Description", "Debit", "Credit"])

def find_unmatched_transactions_by_date(df1, df2):
    """
    Finds unmatched transactions between two DataFrames on the same date.
    """
    unmatched = pd.DataFrame(columns=["Date", "Description", "Debit", "Credit", "Source"])
    
    # Loop through each transaction in df1
    for _, row1 in df1.iterrows():
        # Check for matches in df2 on the same Date, Debit, and Credit
        match = df2[
            (df2["Date"] == row1["Date"]) &
            (df2["Debit"] == row1["Debit"]) &
            (df2["Credit"] == row1["Credit"])
        ]
        
        if match.empty:
            # Add unmatched transaction from df1
            unmatched = pd.concat([unmatched, pd.DataFrame([{
                "Date": row1["Date"],
                "Description": row1["Description"],
                "Debit": row1["Debit"],
                "Credit": row1["Credit"],
                "Source": "File 1"
            }])], ignore_index=True)
    
    # Loop through each transaction in df2
    for _, row2 in df2.iterrows():
        # Check for matches in df1 on the same Date, Debit, and Credit
        match = df1[
            (df1["Date"] == row2["Date"]) &
            (df1["Debit"] == row2["Debit"]) &
            (df1["Credit"] == row2["Credit"])
        ]
        
        if match.empty:
            # Add unmatched transaction from df2
            unmatched = pd.concat([unmatched, pd.DataFrame([{
                "Date": row2["Date"],
                "Description": row2["Description"],
                "Debit": row2["Debit"],
                "Credit": row2["Credit"],
                "Source": "File 2"
            }])], ignore_index=True)
    
    return unmatched

# File paths
file1 = "ReconciledItemsReport.pdf"
file2 = "Search_20112024 - 2 Oct 2024.pdf"

# Extract transactions
df1 = extract_transactions_from_pdf(file1)
df2 = extract_transactions_from_pdf(file2)

# Find unmatched transactions
unmatched_transactions = find_unmatched_transactions_by_date(df1, df2)

# Save the result to an Excel file
output_file = "Unmatched_Transactions_By_Date.xlsx"
unmatched_transactions.to_excel(output_file, index=False)

print(f"Unmatched transactions saved to {output_file}.")