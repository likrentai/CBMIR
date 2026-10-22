"""Table 1 and the category rows of Table 14.

Assigns each fault message to the subsystem it reports on (table1_category_map.csv),
counts onsets per category over the full log and in June 2025, and computes Shannon
entropy across messages and across categories, with and without the blower message.

Run from ANALYSIS3:  python TABLE1_CATEGORIES.py
Reads  build/fault_episodes_v4.csv, OUTPUT/v4/table1_category_map.csv
"""
import collections, csv, math

EPISODES = "build/fault_episodes_v4.csv"
CATMAP = "OUTPUT/v4/table1_category_map.csv"
BLOWER = "AUX CAP MACH RM BLOW1 NOT OFF"
ORDER = ["Ventilation and cooling", "Brakes and pneumatics", "Traction and power conversion",
         "Auxiliary converters and battery", "Power supply and main circuit",
         "Control electronics", "Safety functions"]

cat = {r["message"]: r["category"] for r in csv.DictReader(open(CATMAP, encoding="utf-8"))}
full, june = collections.Counter(), collections.Counter()
for e in csv.DictReader(open(EPISODES, encoding="utf-8")):
    full[e["fault"]] += 1
    if e["onset"].startswith("2025-06"):
        june[e["fault"]] += 1
missing = set(full) - set(cat)
assert not missing, f"messages without a category: {sorted(missing)}"

N, J = sum(full.values()), sum(june.values())
print(f"{N:,} episodes, {len(full)} messages; June 2025: {J} onsets\n")
print(f"{'Category':34s}{'Messages':>9s}{'Full log (%)':>16s}{'June 2025 (%)':>16s}")
for c in ORDER:
    msgs = [m for m in full if cat[m] == c]
    a, b = sum(full[m] for m in msgs), sum(june[m] for m in msgs)
    print(f"{c:34s}{len(msgs):9d}{a:9,d} ({100*a/N:4.1f}){b:9d} ({100*b/J:4.1f})")

def shannon(counts):
    counts = [v for v in counts if v]
    t = sum(counts)
    h = -sum(v / t * math.log2(v / t) for v in counts)
    return h, math.log2(len(counts)), len(counts)

def report(label, counts):
    h, hmax, k = shannon(counts)
    print(f"  {label:34s} H = {h:.3f} bits of {hmax:.3f} (normalised {h/hmax:.3f}, k = {k})")

bycat = collections.Counter(); bycat_nb = collections.Counter()
for m, v in full.items():
    bycat[cat[m]] += v
    if m != BLOWER:
        bycat_nb[cat[m]] += v
print("\nShannon entropy (Table 14)")
report("Fault message", full.values())
report("Fault category (Table 1)", bycat.values())
report("Fault message, without blower", [v for m, v in full.items() if m != BLOWER])
report("Fault category, without blower", bycat_nb.values())
