import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.gridspec import GridSpec
import warnings
warnings.filterwarnings("ignore")

np.random.seed(42)
risks = [
    (1,  "Sales & Trading",                   "Market Risk",            5, 5, 5, 5, 25),
    (2,  "Wealth Management",                  "Credit Risk",            4, 4, 4, 3, 12),
    (3,  "Sales & Trading",                   "Liquidity Risk",         3, 5, 4, 2, 8),
    (4,  "Wealth Management",                  "Operational Risk",       4, 3, 4, 3, 9),
    (5,  "Investment Management",              "Model Risk",             3, 3, 3, 2, 4),
    (6,  "Investment Banking & Capital Mkts",  "Regulatory/Compliance",  3, 5, 4, 2, 8),
    (7,  "Sustainable Investing",              "Reputational Risk",      2, 4, 3, 2, 6),
    (8,  "Wealth Management",                  "Interest Rate Risk",     4, 4, 4, 3, 12),
    (9,  "Sales & Trading",                   "FX Risk",                4, 3, 4, 3, 6),
    (10, "Investment Management",              "Valuation Risk",         3, 4, 4, 2, 8),
    (11, "Sales & Trading",                   "Counterparty Risk",      3, 5, 4, 3, 12),
    (12, "Wealth Management",                  "Cybersecurity Risk",     4, 5, 4, 3, 12),
    (13, "Morgan Stanley at Work",             "Fraud/Theft Risk",       2, 4, 3, 2, 4),
    (14, "Wealth Management",                  "Client Risk",            3, 4, 4, 2, 8),
    (15, "Investment Management",              "Concentration Risk",     3, 3, 3, 2, 4),
    (16, "Investment Management",              "Performance Risk",       3, 4, 4, 3, 9),
    (17, "Investment Banking & Capital Mkts",  "Geopolitical Risk",      5, 4, 4, 3, 12),
    (18, "Investment Banking & Capital Mkts",  "Deal Execution Risk",    3, 3, 3, 2, 4),
    (19, "Research",                           "Forecasting Risk",       3, 2, 3, 3, 6),
    (20, "Sustainable Investing",              "Greenwashing Risk",      1, 5, 3, 1, 4),
    (21, "Sales & Trading",                   "Leverage Risk",          4, 5, 4, 2, 8),
    (22, "Sales & Trading",                   "Commodity Risk",         4, 4, 4, 3, 12),
    (23, "Sales & Trading",                   "Conduct Risk",           3, 4, 4, 2, 6),
    (24, "Morgan Stanley at Work",             "Legal/Tax Risk",         3, 3, 3, 2, 4),
    (25, "Research",                           "IP Risk",                2, 3, 2, 2, 4),
    (26, "Investment Banking & Capital Mkts",  "Competition Risk",       4, 3, 4, 3, 9),
    (27, "Inclusive & Sustainable Ventures",   "Scalability Risk",       3, 3, 3, 3, 6),
]

cols = ["Risk_ID","Sector","Risk_Category",
        "Inherent_Likelihood","Inherent_Impact","Residual_Likelihood","Residual_Impact","Re_Rating"]

df = pd.DataFrame(risks, columns=cols)

# Map scores to labels
likelihood_map = {1:"Rare",2:"Unlikely",3:"Possible",4:"Likely",5:"Almost Certain"}
impact_map     = {1:"Insignificant",2:"Minor",3:"Moderate",4:"Major",5:"Catastrophic"}
rating_map     = {
    25:"Catastrophic", 20:"Very High", 16:"Very High",
    15:"Very High",    12:"High",      9:"High",
    8:"Moderate",      6:"Tolerable",  4:"Low",
    3:"Low",           2:"Low",        1:"Low"
}

df["Inherent_Rating"]  = df["Inherent_Likelihood"] * df["Inherent_Impact"]
df["Residual_Rating"]  = df["Residual_Likelihood"]  * df["Residual_Impact"]
df["Risk_Reduction"]   = df["Inherent_Rating"] - df["Residual_Rating"]

#VAR
n_sim = 100_000

# Simulate daily P&L for key financial risk categories
financial_risks = {
    "Market Risk":       {"mu": -0.0005, "sigma": 0.025},
    "Credit Risk":       {"mu": -0.0003, "sigma": 0.015},
    "Liquidity Risk":    {"mu": -0.0002, "sigma": 0.012},
    "Counterparty Risk": {"mu": -0.0004, "sigma": 0.018},
    "FX Risk":           {"mu": -0.0001, "sigma": 0.010},
    "Interest Rate Risk":{"mu": -0.0002, "sigma": 0.014},
    "Leverage Risk":     {"mu": -0.0006, "sigma": 0.030},
    "Commodity Risk":    {"mu": -0.0003, "sigma": 0.020},
}

portfolio_value = 1_000  # $1,000 mm

var_results = {}
for risk, params in financial_risks.items():
    returns = np.random.normal(params["mu"], params["sigma"], n_sim)
    var_95  = -np.percentile(returns, 5)  * portfolio_value
    var_99  = -np.percentile(returns, 1)  * portfolio_value
    es_95   = -returns[returns <= -var_95 / portfolio_value].mean() * portfolio_value
    var_results[risk] = {"VaR_95": round(var_95, 2),
                         "VaR_99": round(var_99, 2),
                         "ES_95":  round(es_95, 2)}

var_df = pd.DataFrame(var_results).T.reset_index()
var_df.columns = ["Risk_Category","VaR_95 ($mm)","VaR_99 ($mm)","Expected_Shortfall ($mm)"]

scenarios = {
    "Base Case":            {"mkt": 0.00, "credit": 0.00, "liquidity": 0.00, "rates": 0.00},
    "Mild Recession":       {"mkt":-0.15, "credit":-0.10, "liquidity":-0.05, "rates": 0.01},
    "Severe Recession":     {"mkt":-0.35, "credit":-0.25, "liquidity":-0.15, "rates": 0.03},
    "Geopolitical Shock":   {"mkt":-0.20, "credit":-0.12, "liquidity":-0.08, "rates": 0.02},
    "Rate Hike (+300bps)":  {"mkt":-0.12, "credit":-0.08, "liquidity":-0.03, "rates": 0.05},
    "Cyber Attack":         {"mkt":-0.05, "credit":-0.03, "liquidity":-0.10, "rates": 0.00},
    "ESG Regulatory Shock": {"mkt":-0.08, "credit":-0.05, "liquidity":-0.02, "rates": 0.01},
}

weights = {"mkt": 0.40, "credit": 0.25, "liquidity": 0.20, "rates": 0.15}

scenario_results = {}
for scenario, shocks in scenarios.items():
    total_impact = sum(shocks[k] * weights[k] for k in weights) * portfolio_value
    scenario_results[scenario] = round(total_impact, 2)

scenario_df = pd.DataFrame.from_dict(scenario_results, orient="index",
                                      columns=["Portfolio_Impact ($mm)"])
scenario_df["Impact_%"] = (scenario_df["Portfolio_Impact ($mm)"] / portfolio_value * 100).round(2)

stress_scenarios = {
    "2008 GFC":              {"loss_pct": -38.5, "recovery_months": 48},
    "2020 COVID Crash":      {"loss_pct": -33.9, "recovery_months": 6},
    "2022 Rate Shock":       {"loss_pct": -19.4, "recovery_months": 18},
    "2010 Flash Crash":      {"loss_pct":  -9.2, "recovery_months": 3},
    "Russian Default 1998":  {"loss_pct": -20.0, "recovery_months": 24},
    "Dot-com Bust 2000-02":  {"loss_pct": -49.1, "recovery_months": 60},
}

stress_df = pd.DataFrame(stress_scenarios).T.reset_index()
stress_df.columns = ["Scenario","Loss_%","Recovery_Months"]
stress_df["Loss_$mm"] = (stress_df["Loss_%"] / 100 * portfolio_value).round(2)

DARK_BG  = "#0d1b2a"
ACCENT   = "#00bfff"
RED      = "#ff4444"
AMBER    = "#ffaa00"
GREEN    = "#00dd88"
WHITE    = "#e8eaf0"
GRID     = "#1f3045"
PALETTE  = [ACCENT, "#7b68ee", "#00dd88", "#ffaa00", "#ff6b6b", "#da70d6", "#20b2aa", "#f4a460"]

plt.rcParams.update({
    "figure.facecolor":  DARK_BG,
    "axes.facecolor":    DARK_BG,
    "axes.edgecolor":    GRID,
    "axes.labelcolor":   WHITE,
    "axes.titlecolor":   WHITE,
    "xtick.color":       WHITE,
    "ytick.color":       WHITE,
    "text.color":        WHITE,
    "grid.color":        GRID,
    "grid.linewidth":    0.6,
    "font.family":       "DejaVu Sans",
    "font.size":         9,
})

def style_ax(ax, title="", xlabel="", ylabel=""):
    ax.set_facecolor(DARK_BG)
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID)
    ax.grid(True, alpha=0.4)
    if title:  ax.set_title(title,  fontsize=11, fontweight="bold", pad=10, color=WHITE)
    if xlabel: ax.set_xlabel(xlabel, fontsize=9, color=WHITE)
    if ylabel: ax.set_ylabel(ylabel, fontsize=9, color=WHITE)

fig1, ax = plt.subplots(figsize=(12, 8))
fig1.patch.set_facecolor(DARK_BG)
ax.set_facecolor("#0a141f")

grid = np.zeros((5, 5))
risk_color = {
    (1,1):"#1a4a1a",(1,2):"#1a4a1a",(1,3):"#3a5a1a",(1,4):"#5a4a00",(1,5):"#6a3a00",
    (2,1):"#1a4a1a",(2,2):"#3a5a1a",(2,3):"#5a4a00",(2,4):"#6a2a00",(2,5):"#7a1a00",
    (3,1):"#3a5a1a",(3,2):"#5a4a00",(3,3):"#6a3a00",(3,4):"#7a1a00",(3,5):"#8a0000",
    (4,1):"#5a4a00",(4,2):"#6a2a00",(4,3):"#7a1a00",(4,4):"#8a0000",(4,5):"#9a0000",
    (5,1):"#6a3a00",(5,2):"#7a1a00",(5,3):"#8a0000",(5,4):"#9a0000",(5,5):"#aa0000",
}

likelihood_labels = ["Rare","Unlikely","Possible","Likely","Almost\nCertain"]
impact_labels     = ["Insignificant","Minor","Moderate","Major","Catastrophic"]

for (l, i), c in risk_color.items():
    rect = plt.Rectangle([i-1, l-1], 1, 1, color=c, lw=0, zorder=1)
    ax.add_patch(rect)

for _, row in df.iterrows():
    il, ii = row["Inherent_Likelihood"], row["Inherent_Impact"]
    rl, ri = row["Residual_Likelihood"],  row["Residual_Impact"]
    ax.plot(ii - 0.5, il - 0.5, "o", color=RED,   ms=7, zorder=4, alpha=0.85)
    ax.plot(ri - 0.5, rl - 0.5, "D", color=GREEN, ms=5, zorder=5, alpha=0.85)

ax.set_xlim(0, 5); ax.set_ylim(0, 5)
ax.set_xticks([0.5,1.5,2.5,3.5,4.5])
ax.set_yticks([0.5,1.5,2.5,3.5,4.5])
ax.set_xticklabels(impact_labels, fontsize=8.5, color=WHITE)
ax.set_yticklabels(likelihood_labels, fontsize=8.5, color=WHITE)
ax.set_xlabel("Impact →", fontsize=10, color=WHITE, fontweight="bold")
ax.set_ylabel("← Likelihood", fontsize=10, color=WHITE, fontweight="bold")
ax.set_title("Morgan Stanley – Risk Heatmap (All 27 Risks)\nRed circle = Inherent Risk  |  Green diamond = Residual Risk",
             fontsize=12, fontweight="bold", color=WHITE, pad=14)

for spine in ax.spines.values():
    spine.set_edgecolor(GRID)

legend_patches = [
    mpatches.Patch(color="#1a4a1a", label="Low"),
    mpatches.Patch(color="#5a4a00", label="Moderate / Tolerable"),
    mpatches.Patch(color="#7a1a00", label="High / Very High"),
    mpatches.Patch(color="#aa0000", label="Catastrophic"),
]
ax.legend(handles=legend_patches, loc="lower right",
          facecolor="#0d1b2a", edgecolor=GRID, labelcolor=WHITE, fontsize=8)

plt.tight_layout()
fig1.savefig("fig1_heatmap.png", dpi=150, bbox_inches="tight", facecolor=DARK_BG)
plt.close()

fig2, axes = plt.subplots(1, 2, figsize=(14, 6))
fig2.patch.set_facecolor(DARK_BG)
fig2.suptitle("Value at Risk (VaR) Analysis  –  Portfolio Value: $1,000mm",
              fontsize=13, fontweight="bold", color=WHITE, y=1.01)

cats = var_df["Risk_Category"].str.replace(" Risk","",regex=False)

ax = axes[0]
x  = np.arange(len(cats))
w  = 0.35
b1 = ax.bar(x - w/2, var_df["VaR_95 ($mm)"], w, color=ACCENT, alpha=0.85, label="VaR 95%")
b2 = ax.bar(x + w/2, var_df["VaR_99 ($mm)"], w, color=RED,   alpha=0.85, label="VaR 99%")
ax.set_xticks(x); ax.set_xticklabels(cats, rotation=35, ha="right", fontsize=8)
style_ax(ax, "Daily VaR by Risk Category ($mm)", "", "Loss ($mm)")
ax.legend(facecolor=DARK_BG, edgecolor=GRID, labelcolor=WHITE)
for bar in b1: ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2,
                        f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=7, color=WHITE)
for bar in b2: ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.2,
                        f"{bar.get_height():.1f}", ha="center", va="bottom", fontsize=7, color=WHITE)

ax2 = axes[1]
returns_market = np.random.normal(-0.0005, 0.025, n_sim) * portfolio_value
ax2.hist(returns_market, bins=120, color=ACCENT, alpha=0.6, edgecolor="none", density=True)
var95_val = np.percentile(returns_market, 5)
var99_val = np.percentile(returns_market, 1)
ax2.axvline(var95_val, color=AMBER, lw=2, linestyle="--", label=f"VaR 95% = ${abs(var95_val):.1f}mm")
ax2.axvline(var99_val, color=RED,   lw=2, linestyle="--", label=f"VaR 99% = ${abs(var99_val):.1f}mm")
ax2.fill_betweenx([0, ax2.get_ylim()[1] if ax2.get_ylim()[1]>0 else 0.05],
                   returns_market.min(), var99_val, alpha=0.2, color=RED)
style_ax(ax2, "Market Risk P&L Distribution (Monte Carlo)", "Daily P&L ($mm)", "Density")
ax2.legend(facecolor=DARK_BG, edgecolor=GRID, labelcolor=WHITE, fontsize=8)

plt.tight_layout()
fig2.savefig("fig2_var.png", dpi=150, bbox_inches="tight", facecolor=DARK_BG)
plt.close()

fig3, axes = plt.subplots(1, 2, figsize=(14, 6))
fig3.patch.set_facecolor(DARK_BG)
fig3.suptitle("Scenario Analysis & Stress Testing", fontsize=13, fontweight="bold", color=WHITE)

ax = axes[0]
scen_names   = list(scenario_results.keys())
scen_vals    = list(scenario_results.values())
colors_scen  = [GREEN if v >= 0 else AMBER if v > -50 else RED for v in scen_vals]
bars = ax.barh(scen_names, scen_vals, color=colors_scen, alpha=0.85, edgecolor="none")
ax.axvline(0, color=WHITE, lw=0.8, linestyle="-")
style_ax(ax, "Portfolio Impact by Scenario ($mm)", "Impact ($mm)", "")
ax.tick_params(axis="y", labelsize=8.5)
for bar, val in zip(bars, scen_vals):
    xpos = val - 2 if val < 0 else val + 0.5
    ax.text(xpos, bar.get_y() + bar.get_height()/2,
            f"${val:+.1f}mm", va="center", ha="right" if val < 0 else "left",
            fontsize=8, color=WHITE)

ax2 = axes[1]
stress_names  = stress_df["Scenario"].tolist()
stress_losses = stress_df["Loss_$mm"].tolist()
recovery      = stress_df["Recovery_Months"].tolist()
x = np.arange(len(stress_names))
b1 = ax2.bar(x, stress_losses, color=RED, alpha=0.8, label="Portfolio Loss ($mm)")
ax3 = ax2.twinx()
ax3.plot(x, recovery, "D--", color=AMBER, ms=8, lw=2, label="Recovery (months)")
ax3.set_ylabel("Recovery Period (months)", color=AMBER, fontsize=9)
ax3.tick_params(colors=AMBER)
ax3.spines["right"].set_edgecolor(AMBER)
ax2.set_xticks(x); ax2.set_xticklabels(stress_names, rotation=30, ha="right", fontsize=7.5)
style_ax(ax2, "Historical Stress Scenarios", "", "Portfolio Loss ($mm)")
lines1, labs1 = ax2.get_legend_handles_labels()
lines2, labs2 = ax3.get_legend_handles_labels()
ax2.legend(lines1+lines2, labs1+labs2, facecolor=DARK_BG, edgecolor=GRID, labelcolor=WHITE, fontsize=8)

plt.tight_layout()
fig3.savefig("fig3_scenarios.png", dpi=150, bbox_inches="tight", facecolor=DARK_BG)
plt.close()

fig4 = plt.figure(figsize=(16, 10))
fig4.patch.set_facecolor(DARK_BG)
gs = GridSpec(2, 3, figure=fig4, hspace=0.45, wspace=0.38)

ax1 = fig4.add_subplot(gs[0, :2])
sector_g = df.groupby("Sector")[["Inherent_Rating","Residual_Rating"]].mean().sort_values("Inherent_Rating", ascending=True)
short_names = [s[:28] for s in sector_g.index]
x = np.arange(len(sector_g))
ax1.barh(x - 0.2, sector_g["Inherent_Rating"],  0.38, color=RED,   alpha=0.75, label="Inherent Risk")
ax1.barh(x + 0.2, sector_g["Residual_Rating"],   0.38, color=GREEN, alpha=0.75, label="Residual Risk")
ax1.set_yticks(x); ax1.set_yticklabels(short_names, fontsize=8)
style_ax(ax1, "Average Risk Rating: Inherent vs Residual by Sector", "Average Rating (1-25)", "")
ax1.legend(facecolor=DARK_BG, edgecolor=GRID, labelcolor=WHITE, fontsize=8)

ax2 = fig4.add_subplot(gs[0, 2])
cat_counts = df["Risk_Category"].value_counts().head(8)
wedges, texts, autotexts = ax2.pie(
    cat_counts.values, labels=None, autopct="%1.0f%%",
    colors=PALETTE[:len(cat_counts)], startangle=90,
    pctdistance=0.75, wedgeprops={"linewidth":0.5,"edgecolor":DARK_BG}
)
for t in autotexts: t.set_fontsize(7); t.set_color(WHITE)
ax2.legend(cat_counts.index, loc="lower center", bbox_to_anchor=(0.5,-0.25),
           fontsize=6.5, facecolor=DARK_BG, edgecolor=GRID, labelcolor=WHITE, ncol=2)
ax2.set_title("Risk Category Mix", fontsize=10, fontweight="bold", color=WHITE, pad=8)

ax3 = fig4.add_subplot(gs[1, 0])
ax3.bar(var_df["Risk_Category"].str.replace(" Risk","",regex=False),
        var_df["VaR_99 ($mm)"], color=PALETTE, alpha=0.85, edgecolor="none")
ax3.set_xticklabels(var_df["Risk_Category"].str.replace(" Risk","",regex=False),
                     rotation=40, ha="right", fontsize=7)
style_ax(ax3, "VaR 99% by Risk Type ($mm)", "", "$mm")

ax4 = fig4.add_subplot(gs[1, 1])
top10 = df.nlargest(10, "Risk_Reduction")[["Risk_Category","Risk_Reduction"]]
top10_short = top10["Risk_Category"].str.replace(" Risk","",regex=False)
ax4.barh(top10_short, top10["Risk_Reduction"], color=ACCENT, alpha=0.8, edgecolor="none")
style_ax(ax4, "Top 10 Risk Reduction (Controls)", "Rating Points Reduced", "")
ax4.tick_params(axis="y", labelsize=7.5)

ax5 = fig4.add_subplot(gs[1, 2])
bins  = [0,4,8,12,16,26]
labels_bin = ["Low\n(1-4)","Moderate\n(5-8)","High\n(9-12)","Very High\n(13-16)","Critical\n(17+)"]
counts = pd.cut(df["Residual_Rating"], bins=bins, labels=labels_bin).value_counts().sort_index()
colors_bar = [GREEN, ACCENT, AMBER, "#ff8800", RED]
ax5.bar(counts.index, counts.values, color=colors_bar, alpha=0.85, edgecolor="none")
style_ax(ax5, "Residual Risk Distribution", "Rating Band", "No. of Risks")
for i, v in enumerate(counts.values):
    ax5.text(i, v + 0.1, str(v), ha="center", fontsize=9, color=WHITE, fontweight="bold")

fig4.suptitle("Morgan Stanley – Comprehensive Risk Analysis Dashboard",
              fontsize=14, fontweight="bold", color=WHITE, y=1.01)
fig4.savefig("fig4_dashboard.png", dpi=150, bbox_inches="tight", facecolor=DARK_BG)
plt.close()

print("\n── VaR Results ($mm) ──")
print(var_df.to_string(index=False))
print("\n── Scenario Analysis ──")
print(scenario_df.to_string())
print("\n── Stress Test ──")
print(stress_df.to_string(index=False))
