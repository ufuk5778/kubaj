import pandas as pd
import matplotlib.tri as mtri
import json

file_red = "kirmizi.NCN"
file_black = "siyah.NCN"

def load_ncn(path):
    with open(path, "r", encoding="latin1", errors="ignore") as f:
        # İsimlerin (ID) string olarak gelmesi için dtype belirtebiliriz veya sonradan çevirebiliriz
        df = pd.read_csv(
            f,
            delim_whitespace=True,
            header=None,
            comment='#',
            engine="python"
        )
    df = df.iloc[:, :4]           # id, X, Y, Z
    df.columns = ["id", "X", "Y", "Z"]
    return df

red   = load_ncn(file_red)
black = load_ncn(file_black)

# 1. TIN İÇİN EXPORT (Eski fonksiyonunuz)
def export_tin(df, filename):
    tri = mtri.Triangulation(df["X"], df["Y"])
    triangles = []
    for t in tri.triangles:
        p1 = [float(df["X"].iloc[t[0]]), float(df["Y"].iloc[t[0]]), float(df["Z"].iloc[t[0]])]
        p2 = [float(df["X"].iloc[t[1]]), float(df["Y"].iloc[t[1]]), float(df["Z"].iloc[t[1]])]
        p3 = [float(df["X"].iloc[t[2]]), float(df["Y"].iloc[t[2]]), float(df["Z"].iloc[t[2]])]
        triangles.append([p1, p2, p3])
    
    with open(filename, "w") as f:
        json.dump({"triangles": triangles}, f)
    print(f"{filename} oluşturuldu.")

# 2. NOKTALAR VE İSİMLER İÇİN YENİ EXPORT FONKSİYONU 🔹
def export_points(df, filename):
    points = []
    # DataFrame satırlarını gez
    for index, row in df.iterrows():
        
        # 🔹 DÜZELTME BURADA:
        # Önce sayı mı diye kontrol et, sayıysa int() yap, sonra str() çevir.
        raw_id = row["id"]
        try:
            # Eğer sayısal bir değerse (örn: 83.0), tam sayıya (83) çevir
            name = str(int(raw_id))
        except:
            # Eğer "P1", "Nokta-A" gibi harfli bir şeyse olduğu gibi kalsın
            name = str(raw_id)

        points.append({
            "name": name, 
            "coords": [float(row["X"]), float(row["Y"]), float(row["Z"])]
        })
        
    with open(filename, "w") as f:
        json.dump(points, f)
    print(f"{filename} oluşturuldu (isimler düzeltildi).")

# Bu fonksiyonu tanımladıktan sonra tekrar dosyaları oluşturun:
export_points(red,   "red_points.json")
export_points(black, "black_points.json")

# Çalıştır
export_tin(red,    "red_tin.json")
export_tin(black,  "black_tin.json")

# Noktaları da ayrı ayrı veya birleşik çıkarabilirsin.
# Örnek: Sadece kırmızı noktaların isimlerini görmek istiyorsan:
export_points(red, "red_points.json") 
# export_points(black, "black_points.json") # İstersen siyahları da çıkar
# ... (Önceki Python kodlarınızın devamı) ...
