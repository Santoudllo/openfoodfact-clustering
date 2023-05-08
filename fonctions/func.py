import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def selected_features(filepath, threshold, chunksize):
    """
    Selects the columns in the dataset with less than the threshold percent of missing values, and returns the resulting
    dataset with only those columns. Also shows the number of selected columns, the list of the emptiest columns, and
    a heatmap to visualize the missingness of the selected columns.
    Parameters:
    filepath (str): The filepath of the dataset to process.
    threshold (float): The threshold percent of missing values to use for selecting the columns.
    chunksize (int): The size of each chunk to use when reading the dataset.
    Returns:
    selected_df (pandas.DataFrame): The resulting dataset with only the selected columns.
    """

    # Get the number of initial columns
    num_cols = len(pd.read_csv(filepath,header="infer",compression="zip",delimiter= '\t' ,nrows=1).columns)
    print(f"Number of initial columns: {num_cols}")

    # Initialize a dictionary to store the overall missing values for each column
    missing_counts = {col: 0 for col in pd.read_csv(filepath,header="infer" ,compression="zip",delimiter= '\t', nrows=1).columns}

    datalenght= 0
    # Iterate over the dataset in chunks to reduce memory usage
    for chunk in pd.read_csv(filepath, compression="zip",delimiter= '\t',chunksize=chunksize):
        # Calculate the percentage of missing values for each column in the current chunk
        missing = chunk.isnull().sum()
        datalenght += len(chunk)

        # Update the overall missing values for each column by adding by overwriting at each iteration
        for col in missing_counts:
            missing_counts[col] += missing[col]

    # Calculate the overall percentage of missing values for each column
    missing_percentages = pd.Series(missing_counts) / datalenght *100

    # Select the columns that have less than the threshold of missing values
    selected_columns = list(missing_percentages[missing_percentages >= threshold].index)

    # Print the number of selected columns
    print(f"Number of selected columns: {len(selected_columns)}")


    return missing_percentages,selected_columns


def search_componant(df, suffix):
  componant = []
  for col in df.columns:
      if suffix in col: componant.append(col)
  df_subset_columns = df[componant]
  return df_subset_columns


def search_redundant_col(df):
  redundant_columns = []
  for col in df.columns:
    if "_en" in col:
      en = col.replace('_en','')
      tags = col.replace('_en','_tags')
      print("{:<20} 'Sans suffixe' -> {} ; 'Suffixe _tags' -> {}".format(col,
                                                                        en in df.columns, tags in df.columns))
      if en in df.columns : 
        redundant_columns.append(en)
      if tags in df.columns : 
        redundant_columns.append(tags)
  
    if '_tags' in col:
      tags_2 = col.replace('_tags','')
      print("{:<20} 'Suffixe _tags' -> {} ;".format(tags_2, tags_2 in df.columns))
      if tags_2 in df.columns :
        redundant_columns.append(col)

  return redundant_columns