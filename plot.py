import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd

def plot_and_save(field_name: str, station: str, crop: str, kc3: float, df: pd.DataFrame, show: bool = False) -> str:
    # Columns (expects): Date, Bucket, Total Litre, Daily Consumption (Ton)
    df = df.copy()
    df["Date"] = pd.to_datetime(df["Date"])

    # Series
    bucket = df["Bucket"]
    irrigation = df["Total Litre"]
    daily_cons_next = df["Daily Consumption (Ton)"].shift(+1)

    # Figure
    fig, ax = plt.subplots(figsize=(15, 10))

    # Bars
    ax.bar(df["Date"], bucket, label="Bucket")
    ax.bar(df["Date"], irrigation, label="Irrigation", alpha=0.5)

    # Line
    ax.plot(df["Date"], daily_cons_next, label="Daily Consumption (Ton)", color="yellow")

    # Axes & title
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.set_title(f"{field_name} • {station} • {crop} • Weather-Based (Kc3: {kc3})")

    # Date ticks
    ax.xaxis.set_major_locator(mdates.DayLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y-%m-%d"))
    fig.autofmt_xdate()

    # Legend & layout
    ax.legend()
    plt.tight_layout()

    # Output path
    safe_name = "".join(c for c in field_name if c.isalnum() or c in (" ", "_")).strip()
    out_dir = "outputs"
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{safe_name}.png")

    # Save
    plt.savefig(out_path, dpi=150)
    if show:
        plt.show()
    plt.close(fig)

    return out_path
