# MS4S08 CW1 — Housing Affordability in England and Wales

**Module:** MS4S08 Applied Statistics for Data Science
**University:** University of South Wales
---

## Research question

How has housing affordability (median house price to median earnings ratio) changed between 2015 and 2025, and how does Wales compare to England — which local authorities have been affected most?

---

## Data source

| Field | Value |
|---|---|
| Dataset | House price (existing dwellings) to workplace-based earnings ratio |
| Publisher | Office for National Statistics (ONS) |
| Licence | Open Government Licence v3.0 |
| Coverage | Every local authority district in England and Wales, 1997–2025 |
| Format | `.xlsx` workbook, one sheet per analysis type |
| Download | [ONS affordability ratios](https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/housing/datasets/housepriceexistingdwellingstoworkplacebasedearningsratio/current/aff5ratioofhousepriceexistingtoworkplacebasedearnings.xlsx) |

**Harvard reference**

> Office for National Statistics (2026) *House price (existing dwellings) to workplace-based earnings ratio*. Available at: https://www.ons.gov.uk/file?uri=/peoplepopulationandcommunity/housing/datasets/housepriceexistingdwellingstoworkplacebasedearningsratio/current/aff5ratioofhousepriceexistingtoworkplacebasedearnings.xlsx (Accessed: 1 October 2026).

---

## Repository structure

```
.
├── data/
│   ├── aff5ratioofhousepriceexistingtoworkplacebasedearnings.xlsx   # raw ONS workbook
│   └── cleaned_affordability.csv                                    # tidy output from clean_data.py
├── code/
│   └── clean_data.py                                                # Python: reshapes raw ONS data
├── sas/
│   └── analysis.sas                                                 # SAS: all statistical tests
├── powerbi/
│   └── dashboard.pbix                                               # Power BI dashboard
├── poster/
│   └── poster_export.pdf                                            # final A2 poster
└── README.md
```

---

## Data pipeline

### Step 1 — Cleaning (Python)

`code/clean_data.py` reads the ONS workbook, selects the **Table 5c** sheet (local-authority median affordability ratio), reshapes it from wide to long format, and writes `data/cleaned_affordability.csv`.

**Output columns:**

| Column | Description |
|---|---|
| `la_code` | ONS local authority code (e.g. `E06000001`) |
| `local_authority` | Local authority name (e.g. `Hartlepool`) |
| `year` | Year, 1997–2025 |
| `ratio` | Median house price ÷ median workplace-based earnings |
| `region_code` | ONS region code (e.g. `E12000001` for North East, `W92000004` for Wales) |
| `region` | Region name |
| `country` | `England` or `Wales` |

**Dependencies:**

```bash
pip install pandas openpyxl
```

**Run:**

```bash
python code/clean_data.py
```

Rows containing ONS suppression markers (`[x]`) are dropped, since no value is published for those authority-years.

### Step 2 — Statistical analysis (SAS)

Import `cleaned_affordability.csv` into SAS Studio:

```sas
proc import datafile="/path/to/cleaned_affordability.csv"
            out=WORK.AFF dbms=csv replace;
    getnames=yes;
run;
```

Three analyses are run (see `sas/analysis.sas`):

| # | Test | Purpose | SAS procedure |
|---|---|---|---|
| 1 | Wilcoxon signed-rank | Did affordability change between 2015 and 2025 (paired)? | `PROC UNIVARIATE` on paired difference; read the **Signed Rank** row of `Tests for Location: Mu0=0` |
| 2 | Kruskal–Wallis | Does affordability differ across the 10 English regions and Wales in 2025? | `PROC NPAR1WAY WILCOXON` with `CLASS region` |
| 3 | Spearman correlation (optional) | Do expensive areas stay expensive between 2015 and 2025? | `PROC CORR SPEARMAN` on the paired table |

Assumptions are checked first (`PROC UNIVARIATE NORMAL` on paired differences and on 2025 ratios), which justifies the non-parametric approach — normality is rejected for both, largely because a handful of prime central London boroughs have ratios above 20.

### Step 3 — Visualisation (Power BI)

`powerbi/dashboard.pbix` uses the same `cleaned_affordability.csv`. Visuals:

- **Cards** — median ratio in 2015, median ratio in 2025, percentage of local authorities that became less affordable
- **Bar chart** — top 15 least affordable local authorities, 2025
- **Line chart** — affordability trend over time, filtered to Welsh authorities
- **Box plot** — England vs Wales comparison, 2015 and 2025
- **Slicers** — country, year

Screenshots of key visuals are included on the poster.

### Step 4 — Poster (Canva)

A2 portrait poster covering: research question → background and data → methods → exploratory analysis → statistical tests with H₀/H₁ and results → Power BI visuals → key findings → limitations → references. All numbers on the poster come from the SAS and Power BI outputs in this repository.

### Step 5 — Reflective diary (individual)

Not included in this repository; each group member submits their own 500-word reflective piece directly via Blackboard.

---

## Statistical tests — quick reference

| Test | Purpose | SAS |
|---|---|---|
| Wilcoxon signed-rank | Paired change between two years | `PROC UNIVARIATE data=PAIRED; var diff;` → *Signed Rank* row |
| Kruskal–Wallis | Difference across regions (10 groups) | `PROC NPAR1WAY data=AFF wilcoxon; class region; var ratio;` |
| Spearman correlation | Persistence of affordability ranking | `PROC CORR data=PAIRED spearman; var ratio_2015 ratio_2025;` |

---

## Reproducing the analysis

1. Clone the repository.
2. Install Python dependencies: `pip install pandas openpyxl`
3. Run the cleaning script: `python code/clean_data.py`
4. Import the resulting CSV into SAS Studio and run `sas/analysis.sas`.
5. Open `powerbi/dashboard.pbix` in Power BI Desktop and refresh the data source to point to your local copy of `cleaned_affordability.csv`.

---

## Notes and limitations

- The cleaned CSV is derived from the ONS **Table 5c** sheet only — median affordability ratio at local authority level. The raw workbook also contains lower-quartile ratios (Table 6c), separate house price and earnings tables (5a, 5b), county-level data (Tables 3 and 4), and region-level data (Tables 1 and 2). These are available if the analysis is extended, but are not part of the current cleaned dataset.
- Local authority boundaries changed during the period covered (for example the creation of Cornwall, Wiltshire, North Yorkshire, Cumberland, and Westmorland and Furness as unitary authorities). Successor authorities appear only from the year they were established, so time-series comparisons start from 2003 or later for those areas.
- All statistics on the poster are generated from this repository's own code and data.

---

## Licence

Data is © Crown copyright, reproduced under the Open Government Licence v3.0. Analysis code and documentation in this repository are released under the MIT Licence.

---

## Authors

Group project for MS4S08, University of South Wales, 2026–2027.
