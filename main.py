import os
import pandas as pd
import streamlit as st
from modules.rag_tool import initialize_rag_tool, handle_rag_query, save_to_memory as save_rag_memory, load_from_memory as load_rag_memory
from modules.hts_duty_calculator import handle_duty_calculation, export_results_to_file, save_to_memory, load_from_memory
import json

# Suppress TensorFlow warnings
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

# Memory file prefix for individual users
def get_memory_file(user_id, file_type):
    return f"{user_id}_{file_type}_memory.json"

def validate_user_id(user_id):
    """Check if User ID exists in any memory file."""
    rag_file = get_memory_file(user_id, "rag")
    duty_file = get_memory_file(user_id, "duty")
    return os.path.exists(rag_file) or os.path.exists(duty_file)

def suggest_unique_user_id(base_id):
    """Generate a unique User ID if the base ID is taken."""
    counter = 1
    while validate_user_id(base_id):
        base_id = f"{base_id}_{counter}"
        counter += 1
    return base_id

def main():
    st.set_page_config(page_title="HTS AI Agent", layout="wide")

    # Sidebar for user identification and navigation
    st.sidebar.title("HTS AI Agent")
    user_id_input = st.sidebar.text_input("Enter Your User ID:", value="default_user")

    if st.sidebar.button("Validate User ID"):
        if validate_user_id(user_id_input):
            suggested_id = suggest_unique_user_id(user_id_input)
            st.sidebar.warning(f"User ID '{user_id_input}' is already taken. Suggested ID: '{suggested_id}'")
            user_id_input = suggested_id
        else:
            st.sidebar.success(f"User ID '{user_id_input}' is available.")

    if not user_id_input:
        st.error("Please enter a valid User ID to proceed.")
        return

    user_id = user_id_input
    rag_memory_file = get_memory_file(user_id, "rag")
    duty_memory_file = get_memory_file(user_id, "duty")

    menu = st.sidebar.radio("Choose a Tool", ["RAG Tool", "Duty Calculator"])

    if menu == "RAG Tool":
        st.title("RAG Tool")
        initialize_rag_tool()

        # Load user-specific RAG memory
        if "rag_memory" not in st.session_state or st.session_state.get("user_id") != user_id:
            st.session_state.user_id = user_id
            st.session_state.rag_memory = load_rag_memory(rag_memory_file)

        rag_memory = st.session_state.rag_memory

        # User query input
        user_query = st.text_input("Enter your question:")
        if user_query:
            response = handle_rag_query(user_query)
            st.chat_message("user").write(user_query)
            st.chat_message("assistant").write(response)

            # Update memory
            rag_memory.append({"query": user_query, "response": response})
            save_rag_memory(rag_memory, rag_memory_file)
            st.session_state.rag_memory = rag_memory

        # Display query history with delete buttons
        if rag_memory:
            st.write("Query History:")
            for idx, entry in enumerate(rag_memory):
                col1, col2 = st.columns([8, 1])
                with col1:
                    st.write(f"Q: {entry['query']}")
                    st.write(f"A: {entry['response']}")
                with col2:
                    if st.button(f"Delete {idx + 1}", key=f"delete_rag_{idx}"):
                        rag_memory.pop(idx)
                        save_rag_memory(rag_memory, rag_memory_file)
                        st.session_state.rag_memory = rag_memory
                        st.experimental_rerun()

    elif menu == "Duty Calculator":
        st.title("HTS Duty Calculator")

        # Load user-specific duty memory
        if "duty_memory" not in st.session_state or st.session_state.get("user_id") != user_id:
            st.session_state.user_id = user_id
            st.session_state.duty_memory = load_from_memory(duty_memory_file)

        duty_memory = st.session_state.duty_memory

        # Input fields for duty calculation
        hts_code = st.text_input("Enter HTS Code:")
        product_cost = st.number_input("Enter Product Cost ($):", min_value=0.0)
        freight = st.number_input("Enter Freight Cost ($):", min_value=0.0)
        insurance = st.number_input("Enter Insurance Cost ($):", min_value=0.0)

        if st.button("Calculate"):
            result = handle_duty_calculation(hts_code, product_cost, freight, insurance)

            # Update memory with inputs and results
            duty_memory.append({
                "HTS Code": hts_code,
                "Product Cost": product_cost,
                "Freight": freight,
                "Insurance": insurance,
                "Duty Cost": result["Duty Cost"],
                "Total Landed Cost": result["Total Landed Cost"],
            })
            save_to_memory(duty_memory, duty_memory_file)
            st.session_state.duty_memory = duty_memory

            # Display calculation results
            st.write(result)

        # Display memory table with delete buttons
        if duty_memory:
            st.write("Previous Entries:")
            df = pd.DataFrame(duty_memory)
            df.index += 1  # Make index 1-based
            st.dataframe(df)

            for idx in range(len(duty_memory)):
                if st.button(f"Delete {idx + 1}", key=f"delete_duty_{idx}"):
                    duty_memory.pop(idx)
                    save_to_memory(duty_memory, duty_memory_file)
                    st.session_state.duty_memory = duty_memory
                    st.experimental_rerun()

        # Download options
        if st.button("Export to Excel"):
            export_results_to_file(duty_memory, "excel")
            st.success("Results exported to 'duty_results.xlsx'. Check the project directory.")
        if st.button("Export to PDF"):
            export_results_to_file(duty_memory, "pdf")
            st.success("Results exported to 'duty_results.pdf'. Check the project directory.")

if __name__ == "__main__":
    main()
