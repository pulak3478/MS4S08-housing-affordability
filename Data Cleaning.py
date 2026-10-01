import pandas as pd

EXCEL_PATH = r"C:\Users\pulak\Desktop\aff5ratioofhousepriceexistingtoworkplacebasedearnings.xlsx"
OUT_PATH   = r"C:\Users\pulak\Downloads\cleaned_affordability.csv"

# 1. Read — header is on row index 1
df = pd.read_excel(EXCEL_PATH, sheet_name="5c", skiprows=1)

# 2. STRIP whitespace from all column names (this was the bug)
df.columns = [str(c).strip() for c in df.columns]

print("Step 2 — columns after stripping:")
print(list(df.columns))
print()

# 3. Identify ID columns and year columns
id_cols = ["Country/Region code", "Country/Region name",
           "Local authority code", "Local authority name"]

# Confirm all 4 are present
missing = [c for c in id_cols if c not in df.columns]
if missing:
    raise SystemExit(f"Missing id columns: {missing}")

# Year columns: pure digits 1997-2025. Handle 2009.0 -> '2009' style.
def is_year(c):
    s = str(c).strip()
    if s.endswith(".0"):
        s = s[:-2]
    return s.isdigit() and 1997 <= int(s) <= 2025

year_cols = [c for c in df.columns if is_year(c)]
print(f"Step 3 — found {len(year_cols)} year columns")
print()

# 4. Melt wide -> long
long = df.melt(
    id_vars=id_cols,
    value_vars=year_cols,
    var_name="year",
    value_name="ratio"
)

print("Step 4 — columns after melt:")
print(list(long.columns))
print()

# 5. Rename to SAS-friendly names
long = long.rename(columns={
    "Country/Region code": "region_code",
    "Country/Region name": "region",
    "Local authority code": "la_code",
    "Local authority name": "local_authority"
})

print("Step 5 — columns after rename:")
print(list(long.columns))
print()

# 6. Sort so we can see it properly — region first, then LA, then year
long = long.sort_values(["la_code", "year"]).reset_index(drop=True)

# 7. Show the first few rows BEFORE cleaning, so you can verify
print("Step 7 — preview before cleaning:")
print(long[["la_code", "local_authority", "region_code", "region", "year", "ratio"]].head(10))
print()

# 8. Clean: drop [x] and blanks, coerce to numeric
long["ratio"] = pd.to_numeric(long["ratio"], errors="coerce")
long = long.dropna(subset=["ratio"]).reset_index(drop=True)

# 9. Fix year type
long["year"] = long["year"].astype(int)

# 10. Derive country from region code prefix
long["country"] = long["region_code"].str[0].map({"E": "England", "W": "Wales"})

# 11. Final column order for SAS
long = long[["la_code", "local_authority", "year", "ratio",
             "region_code", "region", "country"]]

# 12. Save
long.to_csv(OUT_PATH, index=False)