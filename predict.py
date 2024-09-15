import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

from text import *

import pandas as pd


# DONE
def prepare_data():
  while True:
    print()
    fileType = select_file_type()
    filePath = insert_file_path()
    try:
      if fileType == "csv":
        data = pd.read_csv(filePath)
      elif fileType == "xlsx":
        data = pd.read_excel(filePath)
      print(data.head(10))
      print()
      print("Data Imported Successfully")
      print()
      return data
    except FileNotFoundError:
      print()
      print(f"Error: The file at path '{filePath}' was not found. Please try again.")
    except Exception as e:
      print()
      print(f"An unexpected error happend: {e}")


# DONE
def set_data_index(data):
  print()
  print("TIPS: Column names must be the same as those in the original file")
  print("NOTES: Normally index data in the form of dates to simplify the prediction process")
    
  while True:
    column_name = str(input("-- Enter the column name for the index data: "))
    print()
        
    try:
      data[column_name] = pd.to_datetime(data[column_name])
      data.set_index(column_name, inplace=True)
      print("Index set successfully.")
      return data, column_name
    except KeyError:
      print(f"Error: The column '{column_name}' was not found in the data. Please try again.")
    except Exception as e:
      print(f"An unexpected error occurred: {e}. Please try again.")


#! SKIP
def set_comparison_data_index(data, index_column):
  data[index_column] = pd.to_datetime(data[index_column])
  data.set_index(index_column, inplace=True)
  return data


#! SKIP
def scale_data(data):
  print()
  print("TIPS: Column names must be the same as those in the original file")
    
  while True:
    column_name = str(input("-- Enter the name of the column you want to use for prediction: "))
    print()
    try:
      scaler = MinMaxScaler(feature_range=(0, 1))
      scaled_data = scaler.fit_transform(data[[column_name]])
      print("Data scaled successfully.")
      return scaled_data, scaler, column_name
    except KeyError:
      print(f"Error: The column '{column_name}' was not found in the data. Please try again.")
    except Exception as e:
      print(f"An unexpected error occurred: {e}. Please try again.")


# DONE
def prepare_and_train_model(scaled_data):
  X = scaled_data[:-1]
  y = scaled_data[1:]

  # Train data and test data
  print()
  print("TIPS: Enter a value between 0 and 80 for the test data percentage (Recommended = 20%).")
  print("NOTES: Using more data for testing reduces the data available for training, which can make the model undertrained and underperform. ")

  while True:
    try:
      testing_data_percentage = int(input("-- Enter test data percentage (1-100): "))
      if 1 <= testing_data_percentage <= 100:
        break
      else:
        print()
        print("Error: Please enter a value between 1 and 100.")
        print()
    except ValueError:
      print()
      print("Error: Invalid input! Please enter a valid integer between 1 and 100.")
      print()

  print()
  print(f'Train data = {100 - testing_data_percentage}%')
  print(f'Test data = {testing_data_percentage}%')
  print()
  convert_testing_data_percentage = testing_data_percentage / 100

  X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=convert_testing_data_percentage, shuffle=False)

  model = LinearRegression()
  model.fit(X_train, y_train)

  predicted_price = model.predict(X_test)

  return model, predicted_price


# DONE
def predict_future_prices(scaled_data, model, prediction_days, scaler):
  x_predict = scaled_data[-prediction_days:].reshape(prediction_days, 1)

  predicted_price = model.predict(x_predict)
  predicted_price = scaler.inverse_transform(predicted_price)
    
  return predicted_price

# DONE
def load_comparison_data():
  while True:
    haveComparisonFile = have_comparison_file()
    if haveComparisonFile == 'y':
      fileType = select_comparison_file_type()
      filePath = insert_comparison_file_path()
      
      try:
        if fileType == "csv":
          comparisonData = pd.read_csv(filePath)
        elif fileType == "xlsx":
          comparisonData = pd.read_excel(filePath)
        print(comparisonData.head(10))
        print()
        print("Comparison data imported successfully!")
        print()
        
        return comparisonData, 'y'
      except FileNotFoundError:
        print(f"Error: The file at path '{filePath}' was not found. Please try again.")
      except KeyError as e:
        print(f"Error: The column '{e.args[0]}' was not found in the data. Please try again.")
      except Exception as e:
        print(f"An unexpected error occurred: {e}. Please try again.")
    elif haveComparisonFile == 'n':
      return None, 'n'

#! SKIP
def compare_results(comparison_data, predicted_price, scaledColumnName):
  comparison_data = comparison_data[[scaledColumnName]]
  comparison_data = comparison_data.iloc[:len(predicted_price)]

  if len(comparison_data) != len(predicted_price):
      raise ValueError("Length of predicted prices must match length of data_pembanding")
    
  data_result = pd.DataFrame(index=comparison_data.index)
  data_result['Actual'] = comparison_data[scaledColumnName]
  data_result['Predicted'] = predicted_price.flatten()
    
  return data_result

#! SKIP
def visualize_comparison(comparison_df, prediction_days):
  plt.figure(figsize=(12, 8))
  bar_width = 0.35
  index = range(len(comparison_df.index[:prediction_days]))
    
  actual_prices = comparison_df['Actual'][:prediction_days]
  predicted_prices = comparison_df['Predicted'][:prediction_days]
    
  bar1 = plt.bar([i - bar_width/2 for i in index], actual_prices, bar_width, label='Actual Price')
  bar2 = plt.bar([i + bar_width/2 for i in index], predicted_prices, bar_width, label='Predicted Price')
    
  # Add values on top of each bar
  for bar in bar1:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2,height, f'{height:.2f}', ha='center', va='bottom')
    
  for bar in bar2:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f'{height:.2f}', ha='center', va='bottom')
    
  plt.xlabel('Date')
  plt.ylabel('Price')
  plt.title('Actual vs Predicted Prices')
  plt.xticks(index, comparison_df.index[:prediction_days].strftime('%Y-%m-%d'), rotation=90)
  plt.legend()
    
  plt.show()

#! SKIP
def visualize_predictions(predicted_df):
  plt.figure(figsize=(12, 8))
  bar_width = 0.35
  index = range(len(predicted_df.index))

  predicted_prices = predicted_df['Predicted_Close']
  
  bar = plt.bar(index, predicted_prices, bar_width, label='Predicted Price')
  
  for bar in bar:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height, f'{height:.2f}', ha='center', va='bottom')
  
  plt.xlabel('Date')
  plt.ylabel('Price')
  plt.title('Predicted Prices')
  plt.xticks(index, predicted_df.index.strftime('%Y-%m-%d'), rotation=90)
  plt.legend()
  
  plt.show()