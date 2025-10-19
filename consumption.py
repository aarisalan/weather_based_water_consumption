import pandas as pd
from decimal import Decimal

def calculate_daily_consumption(et0_data, irrigation_data, kc1, kc3, kc4):
    # ET0 → ETc (stage Kc) and daily consumption (ton)
    df_et0 = pd.DataFrame(et0_data, columns=["Date", "Rain", "ET0"]).drop(columns=["Rain"])
    df_et0["ETc1"] = df_et0["ET0"] * Decimal(kc1)
    df_et0["ETc3"] = df_et0["ET0"] * Decimal(kc3)
    df_et0["ETc4"] = df_et0["ET0"] * Decimal(kc4)
    df_et0["Daily Consumption (Ton)"] = df_et0["ETc3"] * 1000 / 1018
    df_et0["Bucket"] = 0
    df_et0.fillna(0, inplace=True)
    df_et0["Date"] = pd.to_datetime(df_et0["Date"]).dt.date

    # Irrigation totals per day (ton)
    cols = [
        "Date",
        "Irrigation Duration Hour",
        "Total Litre",
        "per Hour Litre per 1000m2",
        "Emitter Spacing",
        "Line Count",
        "Line Spacing",
        "Emitter Litre per Hour",
    ]
    df_irrigation_raw = pd.DataFrame(irrigation_data, columns=cols)
    df_irrigation = (
        df_irrigation_raw.loc[:, ["Date", "Total Litre"]]
        .assign(Date=lambda d: pd.to_datetime(d["Date"]).dt.date)
        .groupby("Date", as_index=False, sort=True)["Total Litre"]
        .sum()
    )
    df_irrigation["Total Litre"] = df_irrigation["Total Litre"] / 1018  # to tons

    # Merge & cleanup
    df = (
        pd.merge(df_et0, df_irrigation, on="Date", how="outer")
        .fillna(0)
        .query("`ET0` != 0")
        .reset_index(drop=True)
    )

    return df
