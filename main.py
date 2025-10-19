from process import process_data_and_plot

# Auth (consider using env vars instead of literals)
password = ""

# Device & field identifiers
device_id = 1327
field_name = "Avrupa Tarım / 4. Etap / DTM49 P503/ Sog / Ceviz / Kumlu tın"

# Context (location & crop)
station = "Edirne"
crop = "ceviz"

# Anchor date (YYYY, M, D)
year = 2023
month = 6
day = 16

# Run pipeline (fetch -> compute -> plot/export)
process_data_and_plot(station, crop, device_id, year, month, day, field_name, password)
