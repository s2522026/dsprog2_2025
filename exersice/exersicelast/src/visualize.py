import matplotlib.pyplot as plt
from analyzer import EstatAnalyzer

analyzer = EstatAnalyzer()
df = analyzer.get_by_year(2020)


df = df.dropna(subset=["pref_name", "aging_rate"])
df["aging_rate"] = df["aging_rate"].astype(float)
df["pref_name"] = df["pref_name"].astype(str)

plt.figure(figsize=(8, 6))
plt.barh(df["pref_name"], df["aging_rate"])
plt.xlabel("高齢化率（%）")
plt.title("都道府県別 高齢化率（2020年）")
plt.tight_layout()
plt.show()


analyzer.close()
