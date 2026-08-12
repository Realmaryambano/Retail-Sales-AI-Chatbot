import pandas as pd

july = pd.read_excel("1st July 2026 till 31st July 2026.xlsx")
august = pd.read_excel("1st August 2026 till 10th August 2026.xlsx")

combined = pd.concat([july, august], ignore_index=True)

# Keep date format as DD/MM/YYYY
combined["Transact_Date"] = pd.to_datetime(
    combined["Transact_Date"],
    dayfirst=True
).dt.strftime("%d/%m/%Y")

combined.to_excel(
    "sales_july_1_to_august_10_2026.xlsx",
    index=False
)

print("July rows:", len(july))
print("August rows:", len(august))
print("Combined rows:", len(combined))