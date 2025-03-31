# Mean Threshold Outlier Detection

## Overview

The **Mean Threshold Outlier Detection** program is a statistical tool designed to identify outliers in datasets using a mean-based approach. By assessing the deviation of data points from the mean, the program helps in cleaning datasets by removing outliers, thereby improving the quality of data analysis and modeling.

## Features

- **Mean-Based Outlier Detection**: Utilizes the mean of specified variables to determine whether a data point is an outlier based on a user-defined threshold.
- **Configurable Parameters**: Users can adjust the factor that determines the threshold for outlier detection.
- **Data Listing**: Optionally lists the data in the CSV file, providing insight into the dataset structure.
- **Cleaned Data Output**: Exports a cleaned version of the dataset with outliers removed.

## Requirements

- Python 3.x
- Required libraries:
  - pandas
  - numpy
  - pydantic

You can install the required libraries using pip:

```bash
pip install pandas numpy pydantic

