# CBMIR: fault predictability in locomotive telemetry

Python workflow for the paper

> Tai, L. R., Pandey, A., & Ahn, A. J. *Fault Predictability Across Time Scales in Locomotive Telemetry: A Condition-Based Maintenance Case Study of an Indian Railways Locomotive.* Journal of the Korean Society for Railway (revised manuscript, paper 2026-182).

The study uses one WAP-7 electric locomotive of Indian Railways (unit 37011): a nine-month fault log (4 November 2024 to 21 July 2025) and one month of one-second REMMLOT telemetry (June 2025).

**The data are not included.** The authors do not hold permission to distribute the fault log or the telemetry, so the notebooks document every processing and modelling step but cannot be run without them. Notebook outputs have been cleared for the same reason.

## Order of execution

| No. | File | Purpose | Paper |
|---|---|---|---|
| 01 | `01_INGEST.ipynb` | Parse the telemetry exports; remove duplicate timestamps and simulation-mode records; apply the physical validity specification | 2.5 |
| 02 | `02_REBUILD.ipynb` | Rebuild the fault log from the raw export; apply the explicit exclusion rule for operating events; pair onsets with recoveries into episodes; label the telemetry for the four target windows (D5, W5, W60, W300) | 2.5, 2.7.1 |
| 03 | `03_LABELS.ipynb` | Checks on the labels: unmatched onsets, the D5 post-onset seconds, label variants for the sensitivity analysis, July 2025 labels | 2.5, 2.7.1 |
| 04 | `04_EDA.ipynb` | Daily onset series and most frequent messages | Figure 2; 3.1 |
| 05 | `05_STATS.ipynb` | Descriptive statistics of the daily series; onsets and exposure by operating mode; location changes between onset and recovery | 3.1; Table 5 |
| 06 | `06_MODE_RATE.ipynb` | Onset rates by operating mode (cross-check of Table 5) | Table 5 |
| 07 | `07_CLASSIFY.ipynb` | Label diagnostics and statistics of the measurement channels; classification with Logistic Regression, XGBoost and CatBoost under five class-balancing strategies; feature-set ablation; precision-recall curves | 3.2; Tables 4, 6 to 9; Figures 5, 6 |
| 08 | `08_SEEDS.ipynb` | Every classification configuration over five random seeds (42, 1, 2, 3, 4) | Tables 6 to 8 |
| 09 | `09_MISSING.ipynb` | Sensitivity to the treatment of blanked values (zero fill, forward fill, native missing) | 2.7.1 |
| 10 | `10_UNMATCHED.ipynb` | Sensitivity to the treatment of onsets without a recovery | 2.7.1, 3.2 |
| 11 | `11_CHECK_BLOWER.ipynb` | Results by fault group (blower message, other messages); mode at onset | 3.2; Table 10 |
| 12 | `12_CHECK_BLOWER_TREES.ipynb` | Fixed numbers of trees for the fault groups | 3.2 |
| 13 | `13_CHECK_BLOWER_DETAIL.ipynb` | Operating points and channel importances by fault group | 3.2 |
| 14 | `14_FORECAST.ipynb` | Daily forecasting: SARIMA, LSTM, naive and seasonal naive; dispersion | 3.3; Table 11; Figures 7, 8 |
| 15 | `15_SARIMA.ipynb` | SARIMA specification without seasonal differencing; rolling-origin comparison; residual diagnostics; series without the blower message | 2.7.4, 3.3; Table 11 |
| 16 | `16_ENTROPY.ipynb` | Runs and Ljung-Box tests; Shannon, approximate, sample and permutation entropy; rolling entropy; fault rate against entropy | 3.4; Tables 12 to 14; Figures 9 to 11 |
| 17 | `17_ROUTE.ipynb` | Distance run, onsets per 1,000 km, onsets while moving and standing, leading locations | 3.1, 4.5 |
| 18 | `18_MOVING.ipynb` | Other messages logged while the locomotive was moving | 4.5 |
| 19 | `19_AGEING.ipynb` | Fault rates and mix before and after the annual overhaul; June model scored on July | 4.5 |
| | `TABLE1_CATEGORIES.py` | Table 1 categories (from `table1_category_map.csv`) and the category entropy of Table 14 | Tables 1, 14 |
| | `TABLE3_STATES.py` | Episodes and distinct locations by state (DataMeet state boundaries), joined in QGIS for Figure 4 | Table 3; Figure 4 |
| | `FIG3_NAMED.py` | The twelve most frequent messages with descriptive names | Figure 3 |
| | `table1_category_map.csv` | Assignment of each of the 82 fault messages to a Table 1 category, with onset counts | Table 1 |
| | `CLUSTERS_CHECK.ipynb` | Supplementary: the earlier TF–IDF and k-means clustering and its sensitivity to k, reported in the response to reviewers only | Response to reviewers |

## Folder layout expected by the notebooks

```
ANALYSIS1/DATA/37011/      raw exports (fault log 37011FL.csv, location coordinates 37011GEO.csv)
ANALYSIS2/TELEMETRY/       ingested telemetry (from 01_INGEST)
ANALYSIS3/                 notebooks 02 to 19 and the scripts
ANALYSIS3/DATA/            rebuilt fault log
ANALYSIS3/build/           episodes and labelled telemetry
ANALYSIS3/OUTPUT/v4/       tables and figures
```

Paths are set in the first code cell of each notebook.

## Environment

Python 3.14.3 with pandas, NumPy, SciPy, statsmodels, scikit-learn, XGBoost, CatBoost, imbalanced-learn, antropy and Matplotlib. The LSTM (`14_FORECAST`) runs under Python 3.11 with TensorFlow. `TABLE3_STATES.py` additionally needs shapely. For the same seed, XGBoost row subsampling draws different rows on Windows and Linux builds, so results can differ slightly between platforms; the values in the paper come from the Windows runs.
