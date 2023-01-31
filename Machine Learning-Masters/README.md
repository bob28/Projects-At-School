# Machine Learning (Master's)
#### Machine Learning - final project part 2 
#### November 29, 2021 
**Title:**
Predicting English Premier League Games from Match Statistics

**Goal:**
The goal was to create a 5 page report on any dataset that we want that was created recently, visualize the data using graphs, implement three machine learning algorithms, train and test the data on the models, and then understand which algorithm performed the best using graphs.

**Technologies Used:**
Python, Numpy, Pandas, Excel, Tensorflow, Keras, Scikit-learn, Matplotlib, Plotly

**Result:**
First, I defined the problem and stated the questions that I would like to answer in this report. 

I had to clean and validate the data that I received from [Kaggle](https://www.kaggle.com/datasets/idoyo92/epl-stats-20192020). I imported the CSV into Microsoft Excel and deleted columns and rows that were unnecessary to the end goal. 

I imported the CSV into Pandas and used Numpy to continue getting the data into a workable form. Once that was complete, I went on to create four graphs using Matplotlib to showcase correlations between variables in the dataset. 

The three machine learning algorithms used were: 
- Deep Neural Network (7 layers)
- Linear Regression
- SDG Regressor using Standard Scaler

Then I used Keras and Tensorflow to create these three models. I trained and tested them using a 60-40 split using the scikit-learn *train_test_split* function. 

I used the mean squared error and the mean absolute errors to measure the success of the algorithms. Once that was complete, the linear regression algorithm came out on top and I used the Matplotlib to graph various comparisons between the data and the algorithm on the test data. 

The Python code that was used to do the analysis on can be found in the appendix of the report. 