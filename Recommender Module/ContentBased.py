# -*- coding: utf-8 -*-
"""ContentBased.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1bP8Oqr18rBfLfObMDfPIoigriEmUa396

# Import Data
"""

import pandas as pd
 
courses = pd.read_csv("/Courses.csv")
users = pd.read_csv("/Users.csv")

uid =  1#@param {type:"integer"}
print(uid)

"""# Display datasets"""

users.head(15)

courses.head(8)

"""# Data Cleaning

"""

courses.drop(columns="Unnamed: 3",inplace=True)
courses

courses.dropna(inplace=True)
courses

"""# Get Topic Lists"""

fieldOfInterest = users['field_of_interest'][users['userId']==uid].str.split("|")
userTopics = fieldOfInterest[uid-1]
userTopics

courseCategories = courses['category'].str.split("|").values.tolist()
courseCategories[0]

"""# Output """

for i in range(len(courseCategories)):
  match = list(set(userTopics).intersection(set(courseCategories[i])))
  prob = len(match)/len(courseCategories[i])
  if(prob >0):
   print("probability of "+ courses['title'][courses['courseId']==i+1][i] +" : "+str(prob))