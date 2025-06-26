import pandas as pd
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

Tk().withdraw()
file_path = askopenfilename(title="Please select an Excel file", filetypes=[("Excel files", "*.xlsx *.xls")])

if not file_path:
    print("No file selected. App quitting.")
    exit()

try:
    df = pd.read_excel(file_path)
except Exception as e:
    print(f"Error reading file: {e}")
    exit()

column_map = {
    'What is your ethnicity?': 'Ethnicity',
    'Please specify your gender:': 'Gender',
    'Country/Region': 'Country/Region',
    'State/Province': 'State/Province',
    'In which ward of DC is your business located in?': 'Ward',
    'What is your annual income?': 'Annual Income',
    'Please specify your age:': 'Age'
}

required_columns = list(column_map.keys())

missing = [col for col in required_columns if col not in df.columns]
if missing:
    print(f"The following required columns are missing: {missing}")
    exit()

summary_blocks = []
spacer = pd.DataFrame([["", ""]], columns=["", ""])

for i, col in enumerate(required_columns):
    counts = df[col].value_counts(dropna=False).reset_index()
    counts.columns = [column_map[col], 'Count']
    counts[column_map[col]] = counts[column_map[col]].astype(str)
    summary_blocks.append(counts)

    if i < len(required_columns) - 1:
        summary_blocks.append(spacer)

max_rows = max(len(block) for block in summary_blocks)
summary_blocks = [block.reindex(range(max_rows)) for block in summary_blocks]
summary_df = pd.concat(summary_blocks, axis=1)

output_file = os.path.splitext(file_path)[0] + '_demographic_summary.xlsx'
summary_df.to_excel(output_file, index=False)

os.startfile(output_file)


