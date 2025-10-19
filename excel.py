import os
import pandas as pd

def save_dataframe_to_excel(df: pd.DataFrame, field_name: str) -> str:
    # Clean file-friendly name
    safe_name = "".join(c for c in field_name if c.isalnum() or c in (" ", "_")).strip()

    # Ensure output dir
    out_dir = "outputs"
    os.makedirs(out_dir, exist_ok=True)

    # Write Excel
    out_path = os.path.join(out_dir, f"{safe_name}.xlsx")
    df.to_excel(out_path, index=False)

    # Return path for callers
    return out_path
