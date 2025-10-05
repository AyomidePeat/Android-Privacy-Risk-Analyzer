from androguard.core.bytecodes.apk import APK
import joblib
import os

model_path = "output/risk_model.pkl"
encoder_path = "output/permission_encoder.pkl"
samples_folder = "samples"

model = joblib.load(model_path)
encoder = joblib.load(encoder_path)

def classify_apk(apk_path):
    apk = APK(apk_path)
    permissions = apk.get_permissions()
    X = encoder.transform([permissions])
    pred = model.predict(X)[0]
    print(f"📱 {os.path.basename(apk_path)} → Predicted Risk Level: {pred}")

if __name__ == "__main__":
    apk_files = [f for f in os.listdir(samples_folder) if f.endswith(".apk")]
    if not apk_files:
        print("⚠️ No APK files found in samples/. Please add some.")
    else:
        for apk in apk_files:
            classify_apk(os.path.join(samples_folder, apk))
