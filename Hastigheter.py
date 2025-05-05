import pandas as pd
import numpy as np

# TEORETISK BEREGNING AV HASTIGHETER
rygglegit_tider = [3.3, 3.75, 4.31, 4.24]  # tider i sekunder
sakte_tider = [6.45, 6.73, 6.7, 6.9]  # tider i sekunder
fort1_tider = [2.9, 2.8, 2.8, 2.8]  # tider i sekunder
avstand = 3.0  # meter

def calculate_speed(tider, avstand):
    return [avstand / tid for tid in tider]

rygging_speed_teo = calculate_speed(rygglegit_tider, avstand)
sakte_speed_teo = calculate_speed(sakte_tider, avstand)
fort1_speed_teo = calculate_speed(fort1_tider, avstand)

# BEREGNING AV HASTIGHETER FRA MÅLINGER
rygging_målt = [175, 137.5, 123.5, 120]  # Hz for måling 1-4
sakte_målt = [81.2, 77.4, 78.2, 77.2]  # Hz for måling 1-4
fort1_målt = [175.4, 186.9, 188, 187.3]  # Hz for måling 1-4

f0 = 24.13e9  # Hz

def calculate_speed_from_doppler(frequencies, f0, c=3e8):
    return [(fD * c) / (2 * f0) for fD in frequencies]

rygging_speed_målt = calculate_speed_from_doppler(rygging_målt, f0)
sakte_speed_målt = calculate_speed_from_doppler(sakte_målt, f0)
fort1_speed_målt = calculate_speed_from_doppler(fort1_målt, f0)

# OPPRETTER TABELL MED GJENNOMSNITT OG STANDARDAVVIK
data = {
    "Kategori": ["Rygging", "Sakte", "Fort1"],
    "Teoretisk (m/s)": [np.mean(rygging_speed_teo), np.mean(sakte_speed_teo), np.mean(fort1_speed_teo)],
    "Teo StdAvvik": [np.std(rygging_speed_teo, ddof=1), np.std(sakte_speed_teo, ddof=1), np.std(fort1_speed_teo, ddof=1)],
    "Målt (m/s)": [np.mean(rygging_speed_målt), np.mean(sakte_speed_målt), np.mean(fort1_speed_målt)],
    "Målt StdAvvik": [np.std(rygging_speed_målt, ddof=1), np.std(sakte_speed_målt, ddof=1), np.std(fort1_speed_målt, ddof=1)]
}

df = pd.DataFrame(data)
df = df.round(2)  # Runder av til 2 desimaler

print(df)

# OPPRETTER TABELL MED TEORETISK OG MÅLT FOR HVERT PUNKT
detailed_data = {
    "Kategori": ["Rygging"] * len(rygging_speed_teo) + ["Sakte"] * len(sakte_speed_teo) + ["Fort1"] * len(fort1_speed_teo),
    "Teoretisk (m/s)": [round(teo, 2) for teo in rygging_speed_teo] +
                         [round(teo, 2) for teo in sakte_speed_teo] +
                         [round(teo, 2) for teo in fort1_speed_teo],
    "Målt (m/s)": [round(målt, 2) for målt in rygging_speed_målt] +
                   [round(målt, 2) for målt in sakte_speed_målt] +
                   [round(målt, 2) for målt in fort1_speed_målt]
}

df_detailed = pd.DataFrame(detailed_data)
print(df_detailed)
