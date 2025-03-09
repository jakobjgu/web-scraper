import pandas as pd
import re

input_file_ = "output/scraped_content.txt"
cleaned_txt_file = "output/cleaned_content.txt"
output_file_ = "output/processed_cleaned_content.csv"
output_excel_ = "output/processed_cleaned_content.xlsx"
output_csv_ = "output/occurrence_count.csv"

# Regular expression to match the date format "05-Mar-2025"
date_pattern = re.compile(r"\b\d{2}-[A-Za-z]{3}-\d{4}\b")

def replace_existing_commas(input_txt, output_txt):
    # Read the file, replace commas with underscores, and write back
    with open(input_txt, "r", encoding="utf-8") as file:
        content = file.read().replace(",", "_")
    with open(output_txt, "w", encoding="utf-8") as file:
        file.write(content)

def remove_website_fluff(input_txt):
    start_marker = "(remove)"
    end_marker = "Beneficiary country or territory"

    with open(input_txt, "r", encoding="utf-8") as file:
        lines = file.readlines()

    filtered_lines = []
    skip = False  # Flag to track removal mode

    for line in lines:
        stripped_line = line.strip()

        if stripped_line == start_marker:
            skip = True  # Start skipping lines
        if not skip:
            filtered_lines.append(line)  # Keep lines outside the range
        if stripped_line == end_marker:
            skip = False  # Stop skipping after finding the end marker

    # Write the modified content to a new file
    with open(input_txt, "w", encoding="utf-8") as file:
        file.writelines(filtered_lines)
    print(f"Filtered file saved as {input_txt}")

def add_missing_suppliers(input_txt):
    """ Adds 'no supplier' if the line after 'Open new window' is a date """
   
    with open(input_txt, "r", encoding="utf-8") as file:
        lines = file.readlines()

    modified_lines = []

    for i, line in enumerate(lines):
        stripped_line = line.strip()
        
        modified_lines.append(line)  # Keep current line

        if stripped_line == "Open new window":
            # Check if the next line exists and is a date
            if i + 1 < len(lines) and date_pattern.match(lines[i + 1].strip()):
                modified_lines.append("no supplier\n")  # Insert "no supplier"

    # Save the modified content back to the file
    with open(input_txt, "w", encoding="utf-8") as file:
        file.writelines(modified_lines)

def merge_extra_lines(input_txt):
    """ Ensures only one line remains between 'Open new window' and the next date by merging extra lines. """

    with open(input_txt, "r", encoding="utf-8") as file:
        lines = file.readlines()

    modified_lines = []
    buffer = []  # Temporary storage for lines between 'Open new window' and a date
    merging = False  # Flag to track merging mode

    for i, line in enumerate(lines):
        stripped_line = line.strip()

        if stripped_line == "Open new window":
            # If there was an ongoing merge, finalize it
            if buffer:
                modified_lines.append(" ".join(buffer) + "\n")
                buffer = []

            modified_lines.append(line)  # Keep 'Open new window'
            merging = True  # Start merging process

        elif merging and date_pattern.match(stripped_line):
            # If we hit a date, finalize merging
            if buffer:
                modified_lines.append(" ".join(buffer) + "\n")  # Merge all extra lines
            modified_lines.append(line)  # Keep the date
            buffer = []  # Reset buffer
            merging = False  # Stop merging

        elif merging:
            buffer.append(stripped_line)  # Collect lines to merge

        else:
            modified_lines.append(line)  # Keep all other lines unchanged

    # Handle any leftover buffer
    if buffer:
        modified_lines.append(" ".join(buffer) + "\n")

    # Save the modified content to a new file
    with open(input_txt, "w", encoding="utf-8") as file:
        file.writelines(modified_lines)

def count_lines_between_occurrences(input_txt, output_csv):
    """ 
    Counts the number of lines between occurrences of 'Open new window' 
    and stores the corresponding line indices in a pandas DataFrame.
    """

    with open(input_txt, "r", encoding="utf-8") as file:
        lines = file.readlines()

    line_counts = []
    occurrence_indices = []
    counting = False
    line_count = 0
    last_index = None

    for i, line in enumerate(lines):
        stripped_line = line.strip()
        
        if stripped_line == "Open new window":
            if counting:  # If already counting, store the previous count
                line_counts.append(line_count)
                occurrence_indices.append(last_index)

            line_count = 0  # Reset counter
            counting = True  # Start counting lines
            last_index = i  # Store the index of this occurrence

        else:
            if counting:
                line_count += 1  # Increment counter

    # Convert results to DataFrame
    df = pd.DataFrame({
        "Occurrence Index": occurrence_indices,
        "Lines Between": line_counts
    })

    # Save to CSV
    df.to_csv(output_csv, index=False)
    print(f"Results saved to {output_csv}")

    return df  # Return the DataFrame for further analysis

def remove_open_new_window(input_txt):
    """ Removes all occurrences of 'Open new window' from the text file. """

    with open(input_txt, "r", encoding="utf-8") as file:
        lines = file.readlines()

    # Filter out "Open new window" lines
    cleaned_lines = [line for line in lines if line.strip() != "Open new window"]

    # Save the cleaned content to a new file
    with open(input_txt, "w", encoding="utf-8") as file:
        file.writelines(cleaned_lines)

    print(f"Cleaned file saved as {input_txt}")

def group_six_lines_to_excel(input_txt, output_csv, output_excel):
    with open(input_txt, "r", encoding="utf-8") as infile, open(output_csv, "w", encoding="utf-8") as outfile:
        buffer = []
        
        for line in infile:
            buffer.append(line.strip())  # Remove any leading/trailing spaces or newlines
            
            if len(buffer) == 6:  # Once we have 6 lines, process them
                outfile.write(",".join(buffer) + "\n")  # Join with commas and write to file
                buffer = []  # Reset buffer
        
        # Handle any remaining lines (if total lines are not a multiple of 6)
        if buffer:
            outfile.write(",".join(buffer) + "\n")

    test = pd.read_csv(output_csv)
    # df_cleaned = test.drop_duplicates(keep='first')

    with pd.ExcelWriter(output_excel, engine="openpyxl") as writer:
        test.to_excel(writer, index=False, sheet_name="Sheet1")


replace_existing_commas(input_file_, cleaned_txt_file)
remove_website_fluff(cleaned_txt_file)
add_missing_suppliers(cleaned_txt_file)
merge_extra_lines(cleaned_txt_file)

count_df = count_lines_between_occurrences(cleaned_txt_file, output_csv_)
print(count_df[count_df['Lines Between'] != 6])

remove_open_new_window(cleaned_txt_file)
group_six_lines_to_excel(cleaned_txt_file, output_file_, output_excel_)
