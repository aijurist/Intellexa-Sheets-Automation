import streamlit as st
import csv
import os
import pandas as pd
from io import StringIO

# Department mappings
mappings = {
    "Aeronautical Engineering": "AE",
    "Artificial Intelligence and Data Science": "AI&DS",
    "Artificial Intelligence and Machine Learning": "AI&ML",
    "Automobile Engineering": "AUTO",
    "Biomedical Engineering": "BME",
    "Biotechnology": "BT",
    "Chemical Engineering": "CHE",
    "Civil Engineering": "CIVIL",
    "Computer Science and Design": "CSD",
    "Computer Science and Engineering": "CSE",
    "Computer Science and Engineering (Cyber Security)": "CSE(CS)",
    "Computer Science and Business Systems": "CSBS",
    "Electrical and Electronics Engineering": "EEE",
    "Electronics and Communication Engineering": "ECE",
    "Food Technology": "FT",
    "Information Technology": "IT",
    "Mechanical Engineering": "ME",
    "Mechatronics": "MECHATRONICS",
    "Robotics and Automation": "R&A"
}

def process_csv(file_content, output_file_name, num_extra_columns, extra_headers):
    input_file = StringIO(file_content)
    reader = csv.reader(input_file)
    headers = next(reader)  # Read the header row
    
    selected_columns = [1, 2, 4, 5, 6]  # Column indices for Name, Roll No, Dept, Section, Year
    
    # Create DataFrame to hold the result
    rows = []
    
    for row in reader:
        selected_row = [row[i] for i in selected_columns]
        dept_value = selected_row[2]  # Assuming department is the 3rd column in selected_row (index 2)
        if dept_value in mappings:
            selected_row[2] = mappings[dept_value]  # Replace with the mapped value
        # Add empty columns for extra headers
        for _ in range(num_extra_columns):
            selected_row.append('')  # Add blank values for new columns
        rows.append(selected_row)
    
    # Create DataFrame
    df = pd.DataFrame(rows, columns=[headers[i] for i in selected_columns] + extra_headers)

    # Save to CSV
    output_csv_path = f"./Attendance_sheets/{output_file_name}.csv"
    os.makedirs(os.path.dirname(output_csv_path), exist_ok=True)
    df.to_csv(output_csv_path, index=False)
    
    return df, output_csv_path

# Streamlit UI
st.title("CSV Processor with Department Mapping")

# Upload CSV
uploaded_file = st.file_uploader("Upload CSV", type=["csv"])

if uploaded_file is not None:
    file_content = uploaded_file.getvalue().decode("utf-8")

    # Get Output CSV name
    output_file_name = st.text_input("Enter output CSV file name", value="output")

    # Ask for additional columns
    num_extra_columns = st.number_input("How many additional columns would you like to add?", min_value=0, step=1)

    extra_headers = []
    for i in range(num_extra_columns):
        extra_header = st.text_input(f"Enter header for additional column {i + 1}:")
        extra_headers.append(extra_header)

    # Button to process the CSV
    if st.button("Process CSV"):
        df, output_csv_path = process_csv(file_content, output_file_name, num_extra_columns, extra_headers)
        st.success(f"CSV processing complete. Output saved to {output_csv_path}")
        
        # Show processed CSV in the UI
        st.write("Here is the processed CSV file:")
        st.dataframe(df)

        # Provide download link
        with open(output_csv_path, "rb") as file:
            btn = st.download_button(
                label="Download Processed CSV",
                data=file,
                file_name=f"{output_file_name}.csv",
                mime="text/csv"
            )
