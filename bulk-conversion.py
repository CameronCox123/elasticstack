import json

# Define the input and output file paths
input_file_path = 'C:/path/to/input/file.txt'
output_file_path = 'C:/path/to/output/file.json'
index_name = '[example-index]'

# Read the log data from the file
with open(input_file_path, 'r') as file:
    log_lines = file.readlines()

# Initialize the list to hold formatted lines
bulk_data_lines = []

# Format each log line as a document for bulk upload
for i, line in enumerate(log_lines):
    # Metadata line
    meta_data = { "index": { "_index": index_name, "_id": str(i + 1) } }
    # Document line
    document = { "log_entry": line.strip() }
    # Add the formatted lines to the list
    bulk_data_lines.append(json.dumps(meta_data))
    bulk_data_lines.append(json.dumps(document))

# Write the formatted lines to the output file
with open(output_file_path, 'w') as file:
    file.write('\n'.join(bulk_data_lines))
    file.write('\n')  # Add a newline at the end of the file

print(f"Bulk data has been written to {output_file_path}")

