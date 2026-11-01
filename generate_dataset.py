import pandas as pd
import numpy as np

np.random.seed(42)

data = []

def generate_records(label, count, means, stds):
    for _ in range(count):
        values = np.random.normal(means, stds)

        data.append([
            values[0],
            values[1],
            values[2],
            values[3],
            values[4],
            values[5],
            label
        ])

generate_records(
    "Normal", 160,
    [65, 2, 1500, 6, 3, 7],
    [5, 0.45, 130, 0.8, 1, 1]
)

generate_records(
    "Overheating", 160,
    [96, 2.8, 1350, 6, 7, 11.5],
    [7, 0.7, 170, 1, 1.4, 1.5]
)

generate_records(
    "Excessive Vibration", 160,
    [75, 8, 1450, 5.5, 5, 9],
    [8, 1.3, 180, 1, 1.5, 1.4]
)

generate_records(
    "Tool Wear", 160,
    [82, 4.2, 1100, 7, 9, 10],
    [7, 0.9, 160, 1.1, 1.7, 1.5]
)

generate_records(
    "Misalignment", 160,
    [78, 6, 1250, 4, 6, 9.5],
    [7, 1.1, 170, 0.8, 1.5, 1.4]
)

columns = [
    "temperature_c",
    "vibration_mm_s",
    "spindle_speed_rpm",
    "pressure_bar",
    "operating_hours",
    "power_consumption_kw",
    "defect_type"
]

df = pd.DataFrame(data, columns=columns)

df = df.sample(
    frac=1,
    random_state=42
).reset_index(drop=True)

df.to_csv(
    "data/manufacturing_quality.csv",
    index=False
)

print("Dataset generated successfully!")
print("Total records:", len(df))

print("\nDefect distribution:")
print(df["defect_type"].value_counts())