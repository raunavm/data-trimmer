import csv
import os

def detect_and_trim(input_file, spike_threshold=145):
    if not os.path.isfile(input_file):
        print(f"File '{input_file}' does not exist. Please check the file path and name.")
        return

    with open(input_file, 'r') as infile:
        reader = csv.reader(infile)
        rows = list(reader)

    if len(rows) <= 20:
        print("Not enough data to process.")
        return

    header = rows[0]
    if len(header) < 13:
        print("The CSV does not have enough columns.")
        return

    start_index = 20

    spike_start_index = -1
    baseline_value = None

    for i in range(start_index, len(rows)):
        try:
            current_fz = float(rows[i][12])

            if baseline_value is None:
                baseline_value = current_fz
                continue

            if current_fz - baseline_value >= spike_threshold:
                spike_start_index = i
                print(f"Significant jump detected at row {i} with value {current_fz}.")
                break
        except ValueError:
            print(f"Skipping invalid value in row {i+1}: {rows[i][12]}")
            continue

    if spike_start_index == -1:
        print("There is something wrong with the data.")
        return

    trim_end_index = spike_start_index + 1

    trimmed_rows = [rows[0]]
    trimmed_rows.extend(rows[:start_index])
    trimmed_rows.extend(rows[trim_end_index:])

    with open(input_file, 'w', newline='') as outfile:
        writer = csv.writer(outfile)
        writer.writerows(trimmed_rows)

    print(f"Data trimmed and saved to '{input_file}'")

def main():
    input_file = input("Enter the name of the CSV file: ")
    detect_and_trim(input_file)

if __name__ == "__main__":
    main()
