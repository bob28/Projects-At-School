# Machine Learning (Bachelor's)
#### Machine Learning - final project
#### November 11, 2020
**Title:**
Predicting College Acceptances

**Goal:**
The goal was to create a 5 page report on any dataset that was created recently, visualize the data using graphs, implement three machine learning algorithms, train and test the data on the models, and then understand which algorithm performed the best using graphs.

**Technologies Used:**
Python, Numpy, Pandas, Excel, Tensorflow, Keras, Scikit-learn, Matplotlib, Plotly

**Result:**
First, we defined the problem and stated the questions that we would like to answer in this report. 

We had to clean and validate the data that we received from [Kaggle](https://www.kaggle.com/datasets/mohansacharya/graduate-admissions). We imported the CSV into Microsoft Excel and deleted columns and rows that were unnecessary to the end goal. 

We imported the CSV into Pandas and used Numpy to continue getting the data into a workable form. Once that was complete, we went on to create four graphs using Matplotlib to showcase correlations between variables in the dataset. 

The three machine learning algorithms used were: 
- Deep Neural Network (5 layers)
- Linear Regression
- SDG Regressor using Standard Scaler

Then we used Keras and Tensorflow to create these three models. we trained and tested them using a 50-50 split using the scikit-learn *train_test_split* function. 

We used the mean squared error and the mean absolute errors to measure the success of the algorithms. Once that was complete, the linear regression algorithm came out on top and we used the Matplotlib to graph various comparisons between the data and the algorithm on the test data. 

We also created 2 fake students to determine if they would be admitted into a college using fake standardized testing scores. This allowed us to see how each algorithm could predict change of admission from just scores on exams.

The Python code that was used to do the analysis on can be found in the appendix of the report. 