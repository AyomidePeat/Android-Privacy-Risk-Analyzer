import os
import json
import pandas as pd
from androguard.core.bytecodes.apk import APK

with open("risk_levels.json", "r") as f:
    risk_levels = json.load(f)

def analyze_apk(apk_path):
    apk = APK(apk_path)
    permissions = apk.get_permissions()
    results = []

    for perm in permissions:
        base_perm = perm.split('.')[-1]
        risk = risk_levels.get(perm, "Unknown")
        results.append({"APK": os.path.basename(apk_path), "Permission": perm, "RiskLevel": risk})

    return results

def main():
    folder = "samples"
    output_folder = "output"
    os.makedirs(output_folder, exist_ok=True)
    all_results = []

    for file in os.listdir(folder):
        if file.endswith(".apk"):
            print(f"Analyzing {file} ...")
            apk_path = os.path.join(folder, file)
            results = analyze_apk(apk_path)
            all_results.extend(results)

    df = pd.DataFrame(all_results)
    df.to_csv(os.path.join(output_folder, "risk_summary.csv"), index=False)
    print(" Analysis complete. Saved to output/risk_summary.csv")

if __name__ == "__main__":
    main()
