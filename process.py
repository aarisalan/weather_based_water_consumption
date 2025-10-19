import os
from kc import get_Kc_values
from irrigation import get_irrigation_and_et0_data
from consumption import calculate_daily_consumption
from bucket import calculate_bucket_and_irrigation
from excel import save_dataframe_to_excel
from plot import plot_and_save

def process_data_and_plot(istasyon, urun, device_id, year, month, day, field_name, password):
    # Resolve Kc.csv path
    current_directory = os.path.dirname(__file__)
    kc_csv_path = os.path.join(current_directory, "Kc.csv")

    # Fetch irrigation & ET0
    irrigation_data, et0_data = get_irrigation_and_et0_data(device_id, year, month, day, password)
    
    # Load Kc factors (Kc1, Kc3, Kc4)
    kc1, kc3, kc4 = get_Kc_values(kc_csv_path, istasyon, urun)

    # Compute daily consumption
    df_raw = calculate_daily_consumption(et0_data, irrigation_data, kc1, kc3, kc4)

    # Compute soil bucket & irrigation schedule
    df = calculate_bucket_and_irrigation(df_raw)

    # Export to Excel
    save_dataframe_to_excel(df, field_name)

    # Plot and save figure
    plot_and_save(field_name, istasyon, urun, kc3, df)
