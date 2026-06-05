import pandas as pd

file_path = "d:/Excel/DS Tổng quan Hành vi Tổ chức trong Du lịch OB 253 B-D-F_2.xlsx"
df = pd.read_excel(file_path, sheet_name='DS_THI', header=None)
raw_matrix = df.values.tolist()

print("Looking for time/room info rows:")
for idx, row in enumerate(raw_matrix[:20]):
    clean_cells = []
    for cell in row:
        if pd.isna(cell) or cell is None:
            clean_cells.append("")
        else:
            clean_cells.append(str(cell).strip())
    
    row_combined = " ".join([c.lower() for c in clean_cells if c])
    
    if 'thời gian:' in row_combined or 'thoi gian:' in row_combined:
        print(f"\nRow {idx}: Found time/room info")
        print(f"  clean_cells: {clean_cells}")
        print(f"  Indices: 0='{clean_cells[0]}', 1='{clean_cells[1]}', 2='{clean_cells[2]}', 3='{clean_cells[3]}', 4='{clean_cells[4]}', 5='{clean_cells[5]}', 6='{clean_cells[6]}', 7='{clean_cells[7]}'")
        
        # Check each cell for time and room patterns
        for i, cell_val in enumerate(clean_cells):
            if cell_val:
                val_lower = cell_val.lower()
                print(f"  Cell[{i}]: '{cell_val}'")
                if 'h' in val_lower and '/' in cell_val:
                    print(f"    -> This looks like time")
                if 'quang trung' in val_lower or ('/' in cell_val and 'h' not in val_lower):
                    print(f"    -> This looks like room/location")