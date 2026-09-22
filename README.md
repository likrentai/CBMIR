# CBMIR — Condition-Based Maintenance on Indian Railways

Python workflow for the paper

> **Fault Predictability Across Time Scales in Locomotive Telemetry: A Condition-Based Maintenance Case Study on Indian Railways**
> Submitted to the *Journal of the Korean Society for Railway* (JKSR). The citation will be added on publication.

The study asks whether faults on an electric locomotive can be anticipated from monitoring data the operator already collects, with no additional instrumentation. It uses one-second telemetry and the fault log of a single WAP-7/WAG-9 locomotive (MEDHA propulsion) recorded by the Indian Railways REMMLOT platform. It examines the fault process at two resolutions:

- **Second by second:** does a fault begin within the next 5, 60 or 300 seconds? This is treated as a classification task.
- **Day by day:** can the daily number of fault onsets be forecast, and how regular is the sequence? This is treated as a time-series and entropy analysis.

## Data availability

**The data are not included and cannot be shared.** They belong to Indian Railways, and the authors do not have permission to redistribute them. The notebooks therefore will not run as published. They are provided so that every processing and modelling step can be inspected: how fault episodes and warning windows are defined, how the data are partitioned in time, where resampling is applied, and how each reported figure is computed.

All cell outputs have been cleared for the same reason.

## Notebooks

The notebooks are listed in the order they are run. Section, table and figure numbers refer to the manuscript as submitted.

| Notebook | What it does | Manuscript |
|---|---|---|
| `INGEST.ipynb` | Reads and concatenates the raw REMMLOT telemetry exports. It removes duplicates and simulation records and applies the physical validity specification. Writes `TELEMETRY/build/telemetry_raw_v2.pkl`. | Sections 2.3–2.5 |
| `LABELS.ipynb` | Pairs each fault onset with its recovery to form fault episodes. Builds the warning-window targets (W5, W60, W300) and the detection window (D5); seconds inside an episode are excluded. Writes `telemetry_labelled_v2.pkl` and `fault_episodes_v2.csv`. | Sections 2.2, 2.5, 2.7.1 |
| `EDA.ipynb` | Exploratory analysis of the fault log: daily onsets, the most frequent fault labels, and the location summaries used for the spatial analysis. The state maps were drawn in QGIS. | Section 3.1; Figures 2–3 |
| `STATS.ipynb` | Section 3.1 statistics, fault onsets by operating mode with exposure in hours, and the share of episodes relocated by recovery. | Section 3.1; Table 5 |
| `CLASSIFY.ipynb` | Logistic Regression, XGBoost and CatBoost under five sampling strategies at each window. Uses a chronological three-way split, early stopping on a validation block, and a single scoring of the test partition. Also computes the feature-set ablation and channel importances. | Section 3.2; Tables 6–9; Figures 5–6 |
| `CHECK_BLOWER.ipynb` | Fault-group analysis. Computes the share of the dominant fault label in the study month and the operating mode at onset. Reruns the primary XGBoost on the pooled target, the dominant label alone and the remaining labels. | Section 3.2; Table 10 |
| `CHECK_BLOWER_TREES.ipynb` | Sensitivity check: the same models refitted with a fixed 100 and 300 trees, without early stopping. | Section 3.2 |
| `CHECK_BLOWER_DETAIL.ipynb` | Precision at recall 0.25 and 0.50, and channel importances, for each fault group. | Sections 3.2, 4.2 |
| `FORECAST.ipynb` | Daily fault-count forecasting over a 30-day blind horizon with SARIMA, an LSTM, and naive and seasonal naive baselines. The annual maintenance period is masked. | Section 3.3; Table 11; Figure 7 |
| `ENTROPY.ipynb` | Randomness tests (Wald–Wolfowitz runs, Ljung–Box) and entropy measures (Shannon, approximate, sample and permutation) for the daily series and the fault-label distribution. | Section 3.4; Tables 12–14 |

`INGEST` must run before `LABELS`, and `LABELS` before everything else. `FORECAST` and `ENTROPY` depend only on the fault episodes and are independent of the classification notebooks.

## Expected folder layout

```
ANALYSIS2/
├── DATA/                 raw REMMLOT exports: event-recorder telemetry, fault log, GPS positions (not included)
├── TELEMETRY/build/      intermediate files written by INGEST and LABELS (not included)
├── OUTPUT/               tables and figures written by the analysis notebooks
└── *.ipynb               the notebooks in this repository
```

## Environment

| | |
|---|---|
| Python 3.14.3 | All notebooks except the LSTM |
| Python 3.11.9 | The LSTM in `FORECAST.ipynb` (TensorFlow had no binaries for 3.14 at the time of analysis) |

Main packages: pandas, NumPy, SciPy, statsmodels, antropy, Matplotlib, scikit-learn, XGBoost, CatBoost, imbalanced-learn, TensorFlow and tqdm. Model settings are listed in Table 2 of the manuscript. Hyperparameters are fixed in advance; only the SARIMA orders (by AIC), the number of boosting iterations and the LSTM epochs (by early stopping) are selected. The random seed is 42 throughout.

## Contact

Prof. Lik Ren Tai, Woosong University, Daejeon, Korea.
ORCID [0009-0002-6667-3331](https://orcid.org/0009-0002-6667-3331)
