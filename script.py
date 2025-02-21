
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
warnings.filterwarnings('ignore')
import tkinter as tk
from tkinter import filedialog

root = tk.Tk()
root.withdraw()  # Hide the main window

# Prompt the user to select a file
file_path = filedialog.askopenfilename(title="Select CSV file", filetypes=[("CSV files", "*.csv")])

# Check if a file was selected
if file_path:
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(file_path)
    print("File uploaded successfully and DataFrame created.")
else:
    print("No file selected.")

# Show the data
print(df.head())    
# Format data
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)
# show the the data
print(df.head())
# Create independent variables
df['High-low'] = df['High'] - df['Low']
df['Open-close'] = df['Open'] - df['Close']
# Store the target variable in Y
df['Target'] = np.where(df['Close'].shift(-1) > df['Close'], 1, 0)
# Split the dataset into train and test data
percentage_split = 0.5
row = int(df.shape[0] * percentage_split)
# Train data
X_train = df[['Open-close', 'High-low']][:row]
Y_train = df['Target'][:row]
# Test data
X_test = df[['Open-close', 'High-low']][row:]
Y_test = df['Target'][row:]
# Create and train the SVM model
model = SVC()
model.fit(X_train, Y_train)
# Check the accuracy of the model on the train dataset
train_accuracy = accuracy_score(Y_train, model.predict(X_train))
print("Train Accuracy:", train_accuracy)
# Check the accuracy of the model on the test dataset
test_accuracy = accuracy_score(Y_test, model.predict(X_test))
print("Test Accuracy:", test_accuracy)
# Make predictions and store them in the DataFrame
df['Predictions'] = model.predict(df[['Open-close', 'High-low']])
# Calculate daily returns
df['Return'] = df['Close'].pct_change(1)
# Calculate the strategy returns
df['Strategy_Return'] = df['Predictions'].shift(1) * df['Return']
# Cumulative returns
df['Cumulative_Return'] = df['Return'].cumsum()
# Strategy return
df['Cumulative_Strategy_Return'] = df['Strategy_Return'].cumsum()
# Plotting
plt.figure(figsize=(16, 8))
plt.plot(df.index, df['Cumulative_Return'], label='Cumulative Return', color='blue')
plt.plot(df.index, df['Cumulative_Strategy_Return'], label='Cumulative Strategy Return', color='red')
plt.xlabel('Date')
plt.ylabel('Return')
plt.title('Cumulative Return vs Cumulative Strategy Return')
plt.legend()
plt.show()