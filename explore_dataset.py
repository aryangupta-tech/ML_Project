import pandas as pd

df = pd.read_csv(
    "data/manufacturing_quality.csv"
)

print("First five records:")
print(df.head())

print("\nDataset information:")
print(df.info())

print("\nMissing values:")
print(df.isnull().sum())

print("\nStatistical summary:")
print(df.describe())

print("\nDefect distribution:")
print(df["defect_type"].value_counts())