#from data_scraper import reservations
from pptx import Presentation

template_path = './template.pptx'
prs = Presentation(template_path)

slide = prs.slides[0]

# Loop through shapes in the slide and find the table
for shape in slide.shapes:
    if shape.has_table:
        table = shape.table
        break  # Assuming there's only one table on the slide

# Get the number of rows and columns in the table
num_rows = len(table.rows)
num_cols = len(table.columns)

# Loop through columns first
for col_idx in range(1,num_cols):
    for row_idx in range(1,num_rows):
        cell = table.cell(row_idx, col_idx)
        # Access and modify cell content as needed
        print(cell.text)
