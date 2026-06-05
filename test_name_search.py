import pandas as pd
import re

# Test the search logic from subscription_service.py
file_path = "d:/Excel/DS Tổng quan Hành vi Tổ chức trong Du lịch OB 253 B-D-F_2.xlsx"

print(f"Reading file: {file_path}")
df = pd.read_excel(file_path, sheet_name='DS_THI', header=None)
print(f"Shape: {df.shape}")

# Convert to list for easier inspection
raw_matrix = df.values.tolist()

# Test the name search logic
def test_name_search(search_name):
    search_name_norm = " ".join(search_name.lower().split())
    print(f"\nSearching for: '{search_name}' (normalized: '{search_name_norm}')")
    
    found = []
    for row_list in raw_matrix:
        # Clean cells like in the actual code
        clean_cells = []
        for cell in row_list:
            if pd.isna(cell) or cell is None:
                clean_cells.append("")
            else:
                clean_cells.append(str(cell).strip())
        
        # Check if we have enough columns (changed from >= 4 to >= 5)
        if len(clean_cells) >= 5:
            ho_val = clean_cells[3]  # Changed from [2] to [3]
            ten_val = clean_cells[4]  # Changed from [3] to [4]
            
            # Skip header rows
            if not ho_val or not ten_val or 'họ' in ho_val.lower() or 'tên' in ten_val.lower():
                continue
            
            # Combine name
            full_name_in_file = f"{ho_val} {ten_val}"
            full_name_clean = " ".join(full_name_in_file.lower().split())
            
            # Changed from 'in' to '==' for exact match
            if search_name_norm == full_name_clean:
                found.append(full_name_in_file)
    
    print(f"Found {len(found)} matches")
    for i, name in enumerate(found[:5]):
        print(f"  {i+1}. {name}")
    if len(found) > 5:
        print(f"  ... and {len(found) - 5} more")
    
    return found

# Test cases
print("=" * 60)
test_name_search("Phan Văn An")  # User says this doesn't work
print("=" * 60)
test_name_search("Mai Hoài An")
print("=" * 60)
test_name_search("Ngô Quang An")
print("=" * 60)