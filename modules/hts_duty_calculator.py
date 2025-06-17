import os
import pandas as pd
from fpdf import FPDF
import json
from modules.prepare_db import query_database

MEMORY_FILE = "duty_memory.json"

def handle_duty_calculation(hts_code, product_cost, freight, insurance):
    """Calculate duty and total landed cost."""
    tariff_data = query_database(hts_code)
    if tariff_data.empty:
        return {"Duty Cost": 0.0, "Total Landed Cost": 0.0}

    # Retrieve the duty rate
    duty_rate = tariff_data.iloc[0]["General Rate of Duty"]
    duty_cost = product_cost * duty_rate
    total_cost = product_cost + freight + insurance + duty_cost

    return {"Duty Cost": round(duty_cost, 2), "Total Landed Cost": round(total_cost, 2)}

def export_results_to_file(memory, file_type):
    """Export memory to Excel or PDF."""
    if file_type == "excel":
        df = pd.DataFrame(memory)
        df.to_excel("duty_results.xlsx", index=False)
    elif file_type == "pdf":
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        for entry in memory:
            for key, value in entry.items():
                pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
        pdf.output("duty_results.pdf")

def save_to_memory(memory, file_name):
    """Save memory to a JSON file."""
    with open(file_name, "w") as file:
        json.dump(memory, file)

def load_from_memory(file_name):
    """Load memory from a JSON file."""
    if os.path.exists(file_name):
        with open(file_name, "r") as file:
            return json.load(file)
    return []
