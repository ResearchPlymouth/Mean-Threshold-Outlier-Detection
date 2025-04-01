# Mean Threshold Outlier Detection

## Overview

The **Mean Threshold Outlier Detection** program is a statistical tool designed to identify outliers in datasets using a mean-based approach. By assessing the deviation of data points from the mean, the program helps in cleaning datasets by removing outliers, thereby improving the quality of data analysis and modeling.

## Features

- **Mean-Based Outlier Detection**: Utilizes the mean of specified variables to determine whether a data point is an outlier based on a user-defined threshold.
- **Configurable Parameters**: Users can adjust the factor that determines the threshold for outlier detection.
- **Data Listing**: Optionally lists the data in the CSV file, providing insight into the dataset structure.
- **Cleaned Data Output**: Exports a cleaned version of the dataset with outliers removed.
- **Overlap Removal**: Identifies and removes overlapping constructs based on user-defined constructs and mean differences.
- **Error Handling**: Provides informative error messages for invalid inputs, such as missing constructs or insufficient constructs for overlap checking.

## Requirements

- Python 3.x
- Required libraries:
  - `pandas`
  - `numpy`
  - `pydantic`

You can install the required libraries using pip:

```bash
pip install pandas numpy pydantic
```

## Usage

1. **Prepare Your Data**: Ensure your data is in a CSV format. The first row should contain headers.

2. **Create a Configuration File**: Create a `config.ini` file to define the constructs and data model. An example configuration might look like this:

    ```ini
    [DataModel]
    variable1 = 1
    variable2 = 2

    [Constructs]
    SS = var1, var2, var3
    PEQ = var4, var5
    ```

3. **Run the Program**: Use the command line to run the program with the following syntax:

    ```bash
    python mean_threshold_outlier_detection.py -i path/to/your/input_data.csv -o path/to/output_folder -f factor_value [-m] [-l] [-v] [-r target_constructs] [-th threshold]
    ```

    - `-i`: Path to the input CSV file (required).
    - `-o`: Output folder for cleaned data (default: `cleaned_data`).
    - `-f`: Factor value for analysis (required).
    - `-m`: Perform mean threshold outlier detection (required).
    - `-l`: Optional flag to list the data in the CSV file.
    - `-v`: Optional flag to enable verbose output.
    - `-r`: Comma-separated target constructs to check for overlap (e.g., `SS,PEQ`).

### Example Command

```bash
python mean_threshold_outlier_detection.py -i data.csv -o cleaned_data -f 0.5 -m -r "SS,PEQ" -v
```

This command will perform outlier detection on `data.csv`, using a factor of `0.5`, check for overlap between `SS` and `PEQ`, and output the cleaned data to the specified folder.

## Output

The program will generate a cleaned CSV file in the specified output folder, containing the data without the detected outliers. The output file will be named based on the input filename and factor used.

## Contributing

Contributions are welcome! If you have suggestions for improvements or new features, please open an issue or submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact

For questions or feedback, please contact the maintainer at info@researchplymouth.com.
