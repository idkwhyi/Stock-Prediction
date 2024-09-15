def select_file_type():
  while True:
    print()
    print("Select File Type")
    print("1. CSV")
    print("2. Excel")
    try:
      numberChoice = int(input("-- Enter your choice (in number): "))
      print()
      if numberChoice == 1:
        return "csv"
      elif numberChoice == 2:
        return "xlsx"
      else:
        print()
        print("Invalid number! Please select one of the available numbers.")
    except ValueError:
      print()
      print("Invalid input! Please enter a number.")

def select_comparison_file_type():
  while True:
    print()
    print("Select Comparison File Type")
    print("1. CSV")
    print("2. Excel")
    try:
      numberChoice = int(input("-- Enter your choice (in number): "))
      print()
      if numberChoice == 1:
        return "csv"
      elif numberChoice == 2:
        return "xlsx"
      else:
        print()
        print("Invalid number! Please select one of the available numbers.")
    except ValueError:
      print()
      print("Invalid input! Please enter a number.")


# DONE
def insert_file_path():
  print()
  filePath = str(input("-- Insert file path on your device: "))
  print()
  return filePath

# DONE
def insert_comparison_file_path():
  print()
  filePath = str(input("-- Insert comparison file path on your device: "))
  print()
  return filePath

# * DONE ERROR HANDLING
def have_comparison_file():
  print()
  while True:
    user_input = input("-- Have comparison file?(y/n): ").strip().lower()
    if user_input in ['y', 'n']:
      return user_input
    else:
      print()
      print("Invalid input! Please enter 'y' for yes or 'n' for no.")

      
def continue_or_quit():
  while True:
    print("--#--#--#--#--#--#--#--#--#--#--#--#--")
    print("Do You Want to Continue the Program?")
    print("y = Continue")
    print("n = Quit Program")
    user_choice = input('-- Input your choice (y/n): ')
    
    if user_choice == 'y' or user_choice == 'n':
      return user_choice
    else:
      print()
      print("Invalid Input!")
      print("Please Enter a Valid Choice")
