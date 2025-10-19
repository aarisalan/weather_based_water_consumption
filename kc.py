import pandas as pd

def get_Kc_values(filename, istasyon, urun):
    # Load Kc table
    kc = pd.read_csv(filename)

    # Filter by station & crop
    row = kc[(kc["İstasyon Adı"] == istasyon) & (kc["Ürün"] == urun)]

    # No match → None
    if row.empty:
        print("No data found for the given station and crop.")
        return None

    # Extract factors
    kc1 = row["Kc 1"].values[0]
    kc3 = row["Kc 3"].values[0]
    kc4 = row["Kc 4"].values[0]

    # Return tuple
    return kc1, kc3, kc4
