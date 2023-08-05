import zipfile
import pandas as pd

# ------------------------------------------------------------------------------------------------------------------------------------------

# Function to read .csv files from zip archive
# Output: dictionary, where keys - file name, value - dataset
def read_csv_files_from_zip(zip_archive_path):
    with zipfile.ZipFile(zip_archive_path, 'r') as zip_file:
        # Get the list of CSV files inside the archive
        csv_files = [name for name in zip_file.namelist() if name.endswith('.csv')]
    
        # Create a dictionary to store DataFrames
        dataframes_in_zip = {}
    
        for csv_file in csv_files:
            # Extract the filename without the ".csv" extension
            filename = csv_file
        
            # Read the CSV file and create a DataFrame
            with zip_file.open(csv_file) as file:
                df = pd.read_csv(file)
        
            # Store the DataFrame in the dictionary using the filename as the key
            dataframes_in_zip[filename] = df
            
    return dataframes_in_zip 

# ------------------------------------------------------------------------------------------------------------------------------------------

# Function to print all information about DataFrame
def review_dataframe(df):
    print(" DATA INFO ".center(125,'-'))
    print(df.info())
    
    print(" SHAPE OF DATASET ".center(125,'-'))
    print('Rows:{}'.format(df.shape[0]))
    print('Columns:{}'.format(df.shape[1]))
    
    print(" DATA TYPES ".center(125,'-'))
    print(df.dtypes)
    
    print(" STATISTICS OF DATA ".center(125,'-'))
    print(df.describe(include="all"))
    
    print(" MISSING VALUES ".center(125,'-'))
    print(df.isnull().sum()[df.isnull().sum()>0].sort_values(ascending = False))
    
    print(" DUPLICATED VALUES ".center(125,'-'))
    print(df.duplicated().sum())
    
# ------------------------------------------------------------------------------------------------------------------------------------------

# Function for removing outliers according to its threshold values
def replace_with_threshold(dataframe, variable, percentile, coefficient):
    # Calculation of quantiles according to percentiles
    quartile1 = dataframe[variable].quantile(percentile)
    quartile2 = dataframe[variable].quantile(1-percentile)
    
    # Calculation of interquantile range
    interquantile_range = quartile2 - quartile1
    
    # Calculating thresholds for data
    up_limit = quartile2 + coefficient * interquantile_range
    low_limit = quartile1 - coefficient * interquantile_range
    
    # Interquartile range method to remove outliers from the data 
    # and replaces extreme values with limit values
    dataframe.loc[(dataframe[variable] > up_limit), variable] = up_limit
    dataframe.loc[(dataframe[variable] < low_limit), variable] = low_limit
    
    return dataframe

# ------------------------------------------------------------------------------------------------------------------------------------------