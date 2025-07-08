import pandas as pd

# Path to your large CSV file
input_file = '//filepor10\DOP$\zLoad_MaternityServiceDataset\MSDS 14.01.2025\msds_care_activities_202405_clear_dars_nic_343380_h5q9k.csv'

# Read the file in chunks to determine the total number of rows
chunk_size = 100000  # Adjust based on your system's memory limits
row_count = 0
for chunk in pd.read_csv(input_file, chunksize=chunk_size):
    row_count += len(chunk)

print(row_count)

# Split point
split_row = row_count // 2

# Read and split the file                                    
chunk_iterator = pd.read_csv(input_file, chunksize=chunk_size)
output_file_1 = '//filepor10\DOP$\zLoad_MaternityServiceDataset\MSDS 14.01.2025\msds_care_activities_202405_clear_dars_nic_343380_h5q9k_Part1.csv'
output_file_2 = '//filepor10\DOP$\zLoad_MaternityServiceDataset\MSDS 14.01.2025\msds_care_activities_202405_clear_dars_nic_343380_h5q9k_Part2.csv'

file_encoding = 'utf-8'

# Write the first part
with open(output_file_1, 'w', encoding=file_encoding) as f1:
    written_rows = 0
    for chunk in chunk_iterator:
        if written_rows + len(chunk) <= split_row:
            chunk.to_csv(f1, index=False, header=(written_rows == 0), encoding=file_encoding)  # Write with header for the first chunk
            written_rows += len(chunk)
        else:
            # Write the remaining rows for the first part
            chunk[:split_row - written_rows].to_csv(f1, index=False, header=False, encoding=file_encoding)
            break

# Write the second part
with open(output_file_2, 'w', encoding=file_encoding) as f2:
    # Write the remaining rows of the last chunk and the rest of the file
    chunk[split_row - written_rows:].to_csv(f2, index=False, header=True, encoding=file_encoding)  # Start new file with header
    for chunk in chunk_iterator:
        chunk.to_csv(f2, index=False, header=False, encoding=file_encoding)

print(f"File split into {output_file_1} and {output_file_2} with encoding '{file_encoding}'")