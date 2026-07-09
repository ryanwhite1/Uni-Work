import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


### --- Activity 1 --- ###

student_names = ["Dan", "Meera", "Alissa", "Isaiha", "Nimar"]
student_scores = np.random.randint(0, 100, len(student_names))

student_scores = pd.Series(student_scores, index=student_names)

# Part 1
print(student_scores)

# Part 2
print(student_scores.values[2])

# Part 3
print(student_scores['Alissa'])

# Part 4
print(student_scores.iloc[2], student_scores.loc['Alissa'])

# Part 5
print(student_scores.loc[['Meera', 'Isaiha']])

# Part 6
scores_scaled = student_scores * 1.2
print(scores_scaled)

# Part 7
indices = scores_scaled > 100
scores_scaled[indices] = 100
print(scores_scaled)


# ### --- Activity 2 --- ###

# length = pd.Series(np.array([0.5, 0.75, 1.0, 1.25, 1.5]))
# t_ten = pd.Series(np.array([14.2, 17.3, 20.1, 22.5, 24.6]))
# experiment = pd.Series(np.array(['A', 'B', 'C', 'D', 'E']))

# #then feed in as a list
# data = pd.concat([experiment, length, t_ten], axis='columns')
# #and update the column names as:
# data.columns=['Experiment', 'Length', 'T_ten']

# # Part 1
# # data = pd.DataFrame([[0.5, 14.2], [0.75, 17.3], [1, 20.1], [1.25, 22.5], [1.5, 24.6]], index=['A', 'B', 'C', 'D', 'E'], 
# #                     columns=['length', 'times'])
# print(data)

# data.set_index('Experiment', inplace=True, drop=True)
# print(data)

# # Part 2
# data['ave_time'] = data['T_ten'] / 10

# # Part 3
# data['theoretical'] = 2 * np.pi * np.sqrt(data['Length'] / 9.8)

# # Part 4
# data['rel_error'] = 100 * (data['ave_time'] - data['theoretical']) / data['theoretical']

# # Part 5
# print(data.index[data['rel_error'].abs().argmax()])

# print(data)




### --- Activity 3 --- ###

# # Part 1
# DF = pd.read_csv('Sales.csv')

# # Part 2
# print(DF.head(10))

# # Part 3
# print(DF.info())

# # Part 4
# print(DF['Total_Revenue'].sum())

# # Part 5
# df_cat = DF.groupby('Category')['Total_Revenue'].sum().sort_values()
# print(df_cat)

# # Part 6
# df_prod = DF.groupby('Product_Name')[['Quantity', 'Total_Revenue']].sum()
# print(df_prod['Quantity'].sort_values())
# print(df_prod['Total_Revenue'].sort_values())



# ### --- Activity 4 --- ###

# df = pd.read_csv('Iris_dirty.csv')

# print(df.head(10))

# df_no_stem_length = df.drop(columns='Stem_length')

# #check its gone
# print(df_no_stem_length.info())

# #ok, now let's start dropping NaNs:
# df_no_na = df_no_stem_length.dropna()
# print(df_no_na.info())

# #down to 156 rows -- should be 150!

# #check the values:
# print(df_no_na.describe())

# #ok, can see some weird values:
# # Sepal_length max = 3200!
# # Petal_width max =180!
# # Sepal_width max = 27!
# #Giant flowers or outliers?
# #students should be encouraged to explore the 4 measures
# #using histograms or boxplots to identify outliers and
# #then set up masks to remove:

# # plt.hist(df_no_na['Petal_width'], bins=100)
# # plt.show()
# mask = (df_no_na['Sepal_length'] < 20) & (df_no_na['Sepal_width'] < 20) & (df_no_na['Petal_length'] < 20) & (df_no_na['Petal_width'] < 20)

# df_no_outlier = df_no_na[mask]

# print(df_no_outlier.shape)

# # #still a few extra. Check for duplicate entries using the unique CATID:

# dup_mask = df_no_outlier.duplicated('CATID')
# print(df_no_outlier[dup_mask])

# # #there are three duplicate entries, so we can drop them

# df_no_dup = df_no_outlier.drop_duplicates('CATID')

# print(df_no_dup.shape)

# # #should get 150 rows, as per in class.