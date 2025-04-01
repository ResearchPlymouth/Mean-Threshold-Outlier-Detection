# mean_threshold_outlier_detection.py

from pydantic import BaseModel, conint, ValidationError
import argparse
import configparser
import numpy as np
import os
import pandas as pd

# Function to parse command line arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Mean Threshold Outlier Detection Tool')
    parser.add_argument('-c', '--config', type=str, default='config.ini', help='Path to config.ini file')
    parser.add_argument('-f', '--factor', type=float, help='Factor value for analysis')
    parser.add_argument('-i', '--input_file', type=str, required=True, help='Path to input_data.csv file')
    parser.add_argument('-l', '--list_data', action='store_true', help='List data in the CSV file')
    parser.add_argument('-m', '--mean_threshold_outlier_detect', action='store_true', help='Perform mean threshold outlier detection')
    parser.add_argument('-o', '--output_folder', type=str, default='cleaned_data', help='Output folder for cleaned data')
    parser.add_argument('-r', '--remove_overlapping_constructs', type=str, help='Two target constructs in comma separated for overlap check')
    parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')

    return parser.parse_args()

# Load configuration from config.ini
def load_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)
    return config

# Dynamically create the DataModel class based on config
def create_data_model(config):
    class DynamicDataModel(BaseModel):
        pass

    # Read variable names from the config and add them to the DataModel
    for var_name in config['DataModel']:
        setattr(DynamicDataModel, var_name, conint(ge=1, le=7))
    
    return DynamicDataModel

# Function to list data
def list_data(data, constructs):
    for index, row in data.iterrows():
        construct_data = {
            construct: {var: row[var] for var in vars_list}
            for construct, vars_list in constructs.items()
        }
        # Formatting output without quotes and without np.int64()
        formatted_output = {construct: {var: int(value) for var, value in construct_data[construct].items()} for construct in construct_data}
        print(f"Row #{index + 1}: {formatted_output}")

# Function for mean threshold outlier detection
def mean_threshold_outlier_detect(data, constructs, factor, cleaned_filepath, verbose):
    discarded_rows = []
    cleaned_rows = []

    for index, row in data.iterrows():
        discard = False
        for construct, vars_list in constructs.items():
            values = [row[var] for var in vars_list]
            mean = np.mean(values)
            deviation_threshold = factor * mean
            
            # Format mean to 3 decimal places
            mean_formatted = f"{mean:.3f}"
            
            if verbose:
                # Remove np.int64() and display integer values
                values_formatted = [int(value) for value in values]
                print(f"Checking construct '{construct}' with values: {values_formatted}, mean: {mean_formatted}, threshold: {deviation_threshold:.3f}")

            for value in values:
                if abs(value - mean) > deviation_threshold:
                    discard = True
                    if verbose:
                        print(f"Row #{index + 1}: Value {value} exceeds threshold. Marking for discard.")
                    break

            if discard:
                break  

        if discard:
            discarded_rows.append(index + 1)
        else:
            cleaned_rows.append(row)
            if verbose:
                print(f"Row #{index + 1}: Passed.")

    if verbose:
        print(f"Discarded Rows: {discarded_rows}")

    # Create cleaned DataFrame and export it
    cleaned_data = pd.DataFrame(cleaned_rows)
    cleaned_data.to_csv(cleaned_filepath, index=False)

    return discarded_rows

# Function to remove overlapping constructs
def remove_overlapping_constructs(data, constructs, target_constructs, threshold, cleaned_filepath, verbose):
    discarded_rows = []
    cleaned_rows = []

    # Split the target constructs by comma and strip whitespace
    target_constructs_list = [tc.strip() for tc in target_constructs.split(',')]
    
    # Check if there are at least two constructs
    if len(target_constructs_list) < 2:
        raise ValueError("At least two target constructs must be specified.")

    # Check if all target constructs exist in the constructs dictionary
    for target_construct in target_constructs_list:
        if target_construct not in constructs:
            raise KeyError(f"The construct '{target_construct}' is not found in the constructs dictionary.")

    # Calculate means for the specified constructs
    for index, row in data.iterrows():
        means = [np.mean([row[var] for var in constructs[tc]]) for tc in target_constructs_list]
        mean_diff = abs(means[0] - means[1])  # Compare only the first two constructs for the mean difference

        if verbose:
            print(f"Row #{index + 1}: Means = {[f'{mean:.3f}' for mean in means]}, difference = {mean_diff:.3f}")

        if mean_diff < threshold:
            discarded_rows.append(index + 1)
            if verbose:
                print(f"Row #{index + 1}: Mean difference {mean_diff:.3f} is below threshold. Marking for discard.")
        else:
            cleaned_rows.append(row)
            if verbose:
                print(f"Row #{index + 1}: Passed.")
    
    if verbose:
        print(f"Discarded Rows: {discarded_rows}")

    # Create cleaned DataFrame and export it
    cleaned_data = pd.DataFrame(cleaned_rows)
    cleaned_data.to_csv(cleaned_filepath, index=False)

    return discarded_rows

# Main function
def main():
    # Parse the command line arguments
    args = parse_arguments()
    
    # Load configuration
    config = load_config(args.config)

    # Create the DataModel class
    DynamicDataModel = create_data_model(config)

    # Define constructs
    constructs = {key: value.split(', ') for key, value in config['Constructs'].items()}
    print("Constructs Dictionary:", constructs)

    # Load the input CSV data
    data = pd.read_csv(args.input_file)

    # List data if the flag is set
    if args.list_data:
        list_data(data, constructs)

    # Perform mean threshold outlier detection if the flag is set
    if args.mean_threshold_outlier_detect:
        if args.factor is None:
            print("Factor value is required for mean threshold outlier detection.")
            return
        # Ensure output folder exists
        os.makedirs(args.output_folder, exist_ok=True)
        cleaned_filename = f"{os.path.splitext(os.path.basename(args.input_file))[0]}_{args.factor}_cleaned.csv"
        cleaned_filepath = os.path.join(args.output_folder, cleaned_filename)
        discarded_rows = mean_threshold_outlier_detect(data, constructs, args.factor, cleaned_filepath, args.verbose)

    # Remove overlapping constructs if the flags are set
    if args.remove_overlapping_constructs:
        if args.factor is None:
            print("Factor value is required for remove overlap constructs detection.")
            return
        os.makedirs(args.output_folder, exist_ok=True)
        cleaned_filename = f"{os.path.splitext(os.path.basename(args.input_file))[0]}_{args.remove_overlapping_constructs}_{args.factor}_overlap_cleaned.csv"
        cleaned_filepath = os.path.join(args.output_folder, cleaned_filename)
        discarded_rows = remove_overlapping_constructs(data, constructs, args.remove_overlapping_constructs, args.factor, cleaned_filepath, args.verbose)

if __name__ == "__main__":
    main()
    
    
