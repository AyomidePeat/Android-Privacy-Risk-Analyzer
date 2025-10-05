import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from collections import Counter

input_csv = "output/risk_summary.csv"
output_folder = "output"

df = pd.read_csv(input_csv)
risk_counts = Counter(df["RiskLevel"])
risk_df = pd.DataFrame(risk_counts.items(), columns=["RiskLevel", "Count"])

sns.set(style="whitegrid")
plt.figure(figsize=(8, 5))
sns.barplot(data=risk_df, x="RiskLevel", y="Count", palette="coolwarm")
plt.title("Overall Permission Risk Distribution")
plt.tight_layout()
plt.savefig(os.path.join(output_folder, "risk_chart.png"))
print(" Chart saved to output/risk_chart.png")
