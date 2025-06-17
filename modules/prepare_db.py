import pandas as pd

def query_database(hts_code):
    """Query the database to retrieve tariff data for the given HTS code."""
    file_name = "data/htsdata.csv"
    try:
        tariff_data = pd.read_csv(file_name)
        tariff_data['General Rate of Duty'] = tariff_data['General Rate of Duty'].apply(parse_duty_rate)
        return tariff_data[tariff_data['HTS Number'] == hts_code]
    except FileNotFoundError:
        print(f"Error: '{file_name}' not found.")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error querying database: {e}")
        return pd.DataFrame()

def parse_duty_rate(rate):
    """Parse the duty rate from the CSV."""
    if isinstance(rate, str):
        if rate.lower() == "free":
            return 0.0
        elif '¢' in rate:
            return 0.0
        elif '%' in rate:
            return float(rate.rstrip('%')) / 100
        else:
            try:
                return float(rate)
            except ValueError:
                return 0.0
    return float(rate)
