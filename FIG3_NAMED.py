"""Figure 3: the twelve most frequent fault messages, with descriptive names.

Run from ANALYSIS3:  python FIG3_NAMED.py
Reads build/fault_episodes_v4.csv; writes OUTPUT/v4/top_faults_named.png and .pdf
in the style of 04_EDA."""
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({
    "font.size": 9, "axes.titlesize": 9.5, "axes.labelsize": 9,
    "xtick.labelsize": 8, "ytick.labelsize": 8, "legend.fontsize": 8,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": 0.7, "figure.dpi": 110,
})
NAMES = {
    "AUX CAP MACH RM BLOW1 NOT OFF": "Machine room blower capacitor not switched off",
    "BRAKE CHOPPER GATE LOW VOLTAGE FAULT": "Brake chopper gate low-voltage fault",
    "S/R INTERLOCK - BRAKE COCK": "Start/run interlock: brake cock",
    "IC_DC LINK UNDER VOLTAGE": "Inverter-side DC link undervoltage",
    "S/R INTERLOCK - MAIN RES LOW": "Start/run interlock: main reservoir pressure low",
    "PRIMARY VOLTAGE BELOW MINIMUM": "Primary voltage below minimum",
    "ISOLATION OF AUX CONVERTER3": "Auxiliary converter 3 isolated",
    "EMERGENCY PRESSURE SWITCH ACTING": "Emergency pressure switch acting",
    "DIO2_DOP13 STUCK AT 0": "Output channel 13 of DIO card 2 stuck at 0",
    "EMERGENCY STOP SHUTDOWN": "Emergency stop shutdown",
    "S/R INTERLOCK - AUTO BRAKE": "Start/run interlock: automatic brake",
    "VENTILATION ASCU3 DISTURBED": "Ventilation disturbed (auxiliary converter 3)",
}
ep = pd.read_csv("build/fault_episodes_v4.csv")
vc = ep["fault"].value_counts().head(12)[::-1]
missing = [f for f in vc.index if f not in NAMES]
assert not missing, f"no descriptive name for: {missing}"
share = vc / len(ep) * 100
fig, ax = plt.subplots(figsize=(8, 4))
ax.barh(range(len(vc)), vc.values, color="0.80", zorder=2)
for i, (v, p) in enumerate(zip(vc.values, share.values)):
    ax.text(v + len(ep) * 0.004, i, f"{v:,} ({p:.1f}%)", va="center", fontsize=8, color="0.1")
ax.set_yticks(range(len(vc)))
ax.set_yticklabels([NAMES[f] for f in vc.index], fontsize=8)
ax.set_xlabel("Fault episodes")
ax.set_xlim(0, vc.max() * 1.18)
ax.grid(axis="x", color="0.85", lw=0.5)
plt.tight_layout()
plt.savefig("OUTPUT/v4/top_faults_named.png", dpi=300, bbox_inches="tight")
plt.savefig("OUTPUT/v4/top_faults_named.pdf", bbox_inches="tight")
plt.show()
print(f"{len(ep):,} episodes; top label share {share.iloc[-1]:.1f}%")
