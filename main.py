from predict import *
from text import continue_or_quit


def main():    
  data = prepare_data() # DONE
  data, index_column = set_data_index(data=data) # DONE
    
  scaledData, scaler, scaledColumn = scale_data(data=data) # DONE
  model, predictedPrice = prepare_and_train_model(scaled_data=scaledData) # DONE
    
  # SKIP
  while True:
    try:
      predictionDays = int(input("-- Enter the number of days you want to predict: "))
      if predictionDays > 0:
        break
      else:
        print()
        print("Error: Please enter a positive integer.")
    except ValueError:
      print()
      print("Error: Invalid input! Please enter a valid integer.")
      print()
  predictedPrice = predict_future_prices(scaled_data=scaledData, model=model, prediction_days=predictionDays, scaler=scaler)
  
  # SKIP
  comparisonData, comparisonStatus = load_comparison_data()
    
  if comparisonStatus == 'y':
    # have comparison data
    comparisonData = set_comparison_data_index(data=comparisonData, index_column=index_column)
    dataCompareResult = compare_results(comparison_data=comparisonData, predicted_price=predictedPrice, scaledColumnName=scaledColumn)
    print("Prediction Result")
    print(dataCompareResult)
    visualize_comparison(comparison_df=dataCompareResult, prediction_days=predictionDays)
  else:
    # without comparison data
    predicted_dates = pd.date_range(start=data.index[-1] + pd.Timedelta(days=1), periods=predictionDays)
    predicted_df = pd.DataFrame(predictedPrice, columns=['Predicted_Close'], index=predicted_dates)
    print("Prediction Result")
    print(predicted_df)
    visualize_predictions(predicted_df=predicted_df)
    
    # ask user if they have a comparison file after showing the predictions
    while True:
      print()
      add_comparison = input("-- Do you have a comparison file to add now? (y/n): ").strip().lower()
      print()
      if add_comparison == 'y':
        comparisonData, comparisonStatus = load_comparison_data()
        if comparisonStatus == 'y':
          comparisonData = set_comparison_data_index(data=comparisonData, index_column=index_column)
          dataCompareResult = compare_results(comparison_data=comparisonData, predicted_price=predictedPrice, scaledColumnName=scaledColumn)
          print()
          print("Updated Comparison Result")
          print()
          print(dataCompareResult)
          print()
          visualize_comparison(comparison_df=dataCompareResult, prediction_days=predictionDays)
          print()
        break
      elif add_comparison == 'n':
        break
      else:
        print("Invalid input! Please enter 'y' for yes or 'n' for no.")

# function to run the main program
def run():
  while True:
    main()
    if continue_or_quit() == 'n':
      print()
      print("Exiting program...")
      break

run()