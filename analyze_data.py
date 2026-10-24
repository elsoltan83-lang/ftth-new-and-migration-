import openpyxl
import pandas as pd
import json

excel_file = "FTTH مشروع.xlsx"
wb = openpyxl.load_workbook(excel_file, data_only=True)
sheet = wb["today"]
rows = list(sheet.iter_rows(values_only=True))

headers = [
    "Senior_Sector", "Sector", "Region", "Type",
    "New_Completed_YTD", "New_Survey_Done_YTD", "New_Last_7_Days", "New_Yesterday", "New_Pending_Survey",
    "Migration_Completed_YTD", "Migration_Survey_Done_YTD", "Migration_Last_7_Days", "Migration_Yesterday", "Migration_Pending_Survey",
    "Flagged_2026", "Flagged_Last_7_Days", "Flagged_Yesterday"
]

data = rows[2:] # skipping row 0 (new/migration) and row 1 (subheaders)
df = pd.DataFrame(data, columns=headers)

# Clean numeric columns
num_cols = headers[4:]
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)

summary = {
    "total_rows": len(df),
    "senior_sectors": df["Senior_Sector"].dropna().unique().tolist(),
    "sectors": df["Sector"].dropna().unique().tolist(),
    "regions_count": df["Region"].nunique(),
    "total_new_completed": int(df["New_Completed_YTD"].sum()),
    "total_migration_completed": int(df["Migration_Completed_YTD"].sum()),
    "total_flagged_2026": int(df["Flagged_2026"].sum()),
    "total_migration_yesterday": int(df["Migration_Yesterday"].sum()),
    "total_new_yesterday": int(df["New_Yesterday"].sum())
}

with open("data_summary.json", "w", encoding="utf-8") as f:
    json.dump(summary, f, ensure_ascii=False, indent=2)

print("Data summary saved:", summary)
