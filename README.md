# Morgan Stanley — Enterprise Risk Management Study

A comprehensive risk identification, assessment, and quantitative analysis project covering **27 risks across 8 business sectors** of Morgan Stanley, sourced from the firm's Form 10-Q (Q3 2024).

Applies industry-standard risk frameworks including **Value at Risk (VaR)**, **Monte Carlo simulation**, **scenario analysis**, and **historical stress testing** — modelled in Python and visualised in Excel.

---

## Project Structure

```
morgan-stanley-erm/
│
├── morgan_stanley_risk_analysis.py   # Main Python analysis script
├── build_excel.py                    # Excel workbook generator
│
├── Morgan_Stanley_Risk_Analysis.xlsx # Output: 5-sheet Excel workbook
│
├── fig1_heatmap.png                  # Risk heatmap (inherent vs residual)
├── fig2_var.png                      # VaR & P&L distribution charts
├── fig3_scenarios.png                # Scenario & stress test charts
├── fig4_dashboard.png                # Full risk summary dashboard
│
└── README.md
```

---

## What This Project Does

### 1. Risk Register (`Risk Register` sheet)
- Identifies and documents **27 enterprise risks** across Sales & Trading, Wealth Management, Investment Management, Investment Banking, Sustainable Investing, and more
- Each risk is assessed on **Likelihood × Impact** (1–5 scale) to produce inherent and residual ratings
- Includes risk treatment strategy (Reduce / Accept / Share), monitoring method, and live status
- Colour-coded rating bands: Low → Moderate → High → Very High → Catastrophic

### 2. Value at Risk — VaR (`VaR Analysis` sheet + `fig2_var.png`)
- Runs a **Monte Carlo simulation** (N = 100,000) for 8 financial risk categories
- Computes **VaR at 95% and 99% confidence levels** and **Expected Shortfall (CVaR)**
- Plots the full P&L return distribution with tail-risk shading for Market Risk
- Assumes a reference portfolio value of $1,000mm

### 3. Scenario Analysis (`Scenario Analysis` sheet + `fig3_scenarios.png`)
- Models portfolio impact across **7 macro scenarios**: Base Case, Mild Recession, Severe Recession, Geopolitical Shock, Rate Hike (+300bps), Cyber Attack, ESG Regulatory Shock
- Uses a weighted driver model across market, credit, liquidity, and interest rate shocks
- Worst case: Severe Recession → **-$228mm (-22.8%)** portfolio impact

### 4. Stress Testing (`Stress Testing` sheet + `fig3_scenarios.png`)
- Applies **6 historical drawdown events** to the reference portfolio
- Includes: 2008 GFC, 2020 COVID crash, 2022 rate shock, 2010 flash crash, 1998 Russian default, 2000–02 dot-com bust
- Tracks both portfolio loss ($mm) and estimated recovery period (months)
- Worst case: Dot-com bust → **-$491mm** with a 60-month recovery

### 5. Risk Summary Dashboard (`Risk Summary` sheet + `fig4_dashboard.png`)
- KPI cards: total risks, critical risks, treatment coverage, average risk reduction
- Top 10 risks ranked by inherent rating with reduction achieved post-controls
- Sector-level inherent vs residual comparison
- Residual risk distribution across rating bands

---

## Visualisations

| Chart | Description |
|-------|-------------|
| `fig1_heatmap.png` | 5×5 risk heatmap — red circles (inherent), green diamonds (residual) |
| `fig2_var.png` | VaR bar chart + Monte Carlo P&L distribution with tail shading |
| `fig3_scenarios.png` | Scenario waterfall + historical stress test dual-axis chart |
| `fig4_dashboard.png` | Multi-panel dashboard: sector ratings, VaR, risk reduction, distribution |

---

## Tech Stack

| Tool | Usage |
|------|-------|
| `Python 3.10+` | Core scripting and modelling |
| `NumPy` | Monte Carlo simulation, VaR/CVaR calculation |
| `Pandas` | Risk register data manipulation and aggregation |
| `Matplotlib` | Chart generation (4 publication-quality figures) |
| `openpyxl` | Excel workbook creation with formatting and formulas |

---

## Getting Started

### Prerequisites
```bash
pip install numpy pandas matplotlib openpyxl
```

### Run the Python analysis
```bash
python3 morgan_stanley_risk_analysis.py
```
Outputs 4 PNG charts in the current directory.

### Generate the Excel workbook
```bash
python3 build_excel.py
```
Outputs `Morgan_Stanley_Risk_Analysis.xlsx` with 5 fully formatted sheets.

---

## Data Source

> Morgan Stanley Form 10-Q, Q3 2024
> https://www.morganstanley.com/content/dam/msdotcom/en/about-us-ir/shareholder/10q0924.pdf

All quantitative parameters (volatility, drift, scenario shocks) are illustrative estimates used for educational and analytical modelling purposes. This project is not affiliated with or endorsed by Morgan Stanley.

---

## Key Findings

- **Market Risk** holds the highest inherent score (25/25) — daily VaR 99% = $58.87mm
- **Leverage Risk** carries the highest simulated VaR at $70.61mm (99%) due to elevated volatility
- **Geopolitical Risk** rated *Almost Certain* likelihood — the only non-financial risk in the top tier
- **Cybersecurity** is the only risk under active real-time monitoring
- Controls reduce average risk rating by **5.6 points** — 9 risks remain High or above post-treatment
- A Severe Recession scenario would cost an estimated **-$228mm**, stress-tested against Basel III capital thresholds

---

## Author

Developed as part of Enterprise Risk Management (ERM) coursework, where the original requirement was limited to a risk register, but extended into a comprehensive quantitative risk analysis using VaR, Monte Carlo simulation, and scenario modeling.
