import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
import os

# Paths
input_csv = "output/risk_summary.csv"
output_folder = "output"
pdf_file = os.path.join(output_folder, "Privacy_Risk_Report.pdf")

# Load data
df = pd.read_csv(input_csv)

# Compute per-app risk summary
summary = df.groupby(["APK", "RiskLevel"]).size().unstack(fill_value=0)
summary["Total"] = summary.sum(axis=1)
summary["High%"] = (summary.get("High", 0) / summary["Total"] * 100).round(1)
summary["Medium%"] = (summary.get("Medium", 0) / summary["Total"] * 100).round(1)
summary["Low%"] = (summary.get("Low", 0) / summary["Total"] * 100).round(1)

# Global chart
plt.figure(figsize=(8,5))
df["RiskLevel"].value_counts().plot(kind='bar', color=['#e74c3c', '#f1c40f', '#2ecc71', '#95a5a6'])
plt.title("Overall Permission Risk Distribution", fontsize=14)
plt.xlabel("Risk Level")
plt.ylabel("Count")
plt.tight_layout()
chart_path = os.path.join(output_folder, "overall_risk_chart.png")
plt.savefig(chart_path)
plt.close()

# PDF generation
styles = getSampleStyleSheet()
doc = SimpleDocTemplate(pdf_file, pagesize=A4)
story = []

story.append(Paragraph("<b>Android Privacy Risk Analysis Report</b>", styles["Title"]))
story.append(Spacer(1, 12))
story.append(Paragraph("This report summarizes permission-based privacy risks detected across analyzed Android applications. Each permission is categorized as Low, Medium, or High risk based on its access level and data sensitivity.", styles["Normal"]))
story.append(Spacer(1, 20))

story.append(Image(chart_path, width=400, height=250))
story.append(Spacer(1, 20))

story.append(Paragraph("<b>Per-App Privacy Summary</b>", styles["Heading2"]))
story.append(Spacer(1, 12))

# Add table
data = [summary.reset_index().columns.tolist()] + summary.reset_index().values.tolist()
table = Table(data)
table.setStyle(TableStyle([
    ('BACKGROUND', (0,0), (-1,0), colors.grey),
    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
    ('ALIGN', (0,0), (-1,-1), 'CENTER'),
    ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
    ('BOTTOMPADDING', (0,0), (-1,0), 12),
    ('GRID', (0,0), (-1,-1), 0.25, colors.black),
]))
story.append(table)
story.append(Spacer(1, 20))

story.append(Paragraph("Apps with higher percentages of High-risk permissions may access sensitive user data such as location, contacts, or microphone. These should be carefully reviewed before installation.", styles["Italic"]))
story.append(Spacer(1, 20))

story.append(Paragraph("<b>Generated automatically by PrivacyRiskAnalyzer v1.0</b>", styles["Normal"]))
story.append(Spacer(1, 10))
story.append(Paragraph("© 2025 OLADIPUPO PEACE", styles["Normal"]))

doc.build(story)
print(f"✅ Privacy risk report generated: {pdf_file}")
