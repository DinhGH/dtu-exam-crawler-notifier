import pandas as pd

file_path = "d:/Excel/DS Tổng quan Hành vi Tổ chức trong Du lịch OB 253 B-D-F_2.xlsx"
df = pd.read_excel(file_path, sheet_name='DS_THI', header=None)

# Get the row with "Phan Văn An"
raw_matrix = df.values.tolist()

print("Excel structure (first 15 columns of row 4):")
print("Index | Value")
print("-" * 50)

for i, cell in enumerate(raw_matrix[4][:15]):
    print(f"{i:5} | '{cell}'")

print("\n\nLooking for Phan Văn An row:")
for idx, row in enumerate(raw_matrix[:10]):
    clean_cells = []
    for cell in row:
        if pd.isna(cell) or cell is None:
            clean_cells.append("")
        else:
            clean_cells.append(str(cell).strip())
    
    print(f"\nRow {idx}:")
    if len(clean_cells) >= 5:
        print(f"  0 (STT): '{clean_cells[0]}'")
        print(f"  1 (Mã SV): '{clean_cells[1]}'")
        print(f"  2 (Họ): '{clean_cells[2]}'")
        print(f"  3 (Tên): '{clean_cells[3]}'")
        print(f"  4 (Lớp): '{clean_cells[4]}'")
    
    # Check if this is the Phan Văn An row
    if len(clean_cells) >= 4:
        ho = clean_cells[2]
        ten = clean_cells[3]
        if 'Phan' in ho and 'Văn' in ho:
            print(f"  -> FOUND Phan Văn: '{ho} {ten}'")
        if 'Phan' in ho and 'Văn' in ho and 'An' in ten:
            print(f"  -> FOUND Phan Văn An: '{ho} {ten}'")