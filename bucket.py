import pandas as pd

def calculate_bucket_and_irrigation(df: pd.DataFrame) -> pd.DataFrame:
    # Rolling water bucket (ton) based on previous day balance, irrigation, and consumption
    for i in range(1, len(df)):
        prev_bucket = float(df.loc[i - 1, "Bucket"])
        prev_irrig = float(df.loc[i - 1, "Total Litre"])
        prev_cons  = float(df.loc[i - 1, "Daily Consumption (Ton)"])

        # Daily bucket = yesterday bucket + irrigation - consumption
        curr_bucket = prev_bucket + prev_irrig - prev_cons

        # Reset rule: if irrigation applied yesterday, bucket equals that irrigation
        if prev_irrig > 0:
            curr_bucket = prev_irrig

        # Carry today’s irrigation value forward (kept as-is)
        df.loc[i, "Bucket"] = curr_bucket
        df.loc[i, "Total Litre"] = df.loc[i, "Total Litre"]

    # Round numeric outputs for presentation
    for col in ["ET0", "ETc1", "ETc3", "ETc4", "Daily Consumption (Ton)", "Bucket", "Total Litre"]:
        if col in df.columns:
            df[col] = df[col].astype(float).round(4)

    return df
