import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ### --- Activity 1 --- ###

# students = ['Dan', 'Meera', 'Alissa', 'Isaiha', 'Nimar']
# scores = np.random.randint(0, 101, len(students))

# student_scores = pd.Series(scores, index=students)

# # Part 1
# print(student_scores)

# # Part 2
# print(student_scores.values[2])

# # Part 3
# print(student_scores['Alissa'])

# # Part 4
# print(student_scores.loc['Alissa'], student_scores.iloc[2])

# # Part 5
# print(student_scores.loc[['Meera', 'Isaiha']])

# # Part 6
# student_scores *= 1.2
# print(student_scores)

# # Part 7
# mask = student_scores > 100
# student_scores[mask] = 100
# print(student_scores)





# ### --- Activity 2 --- ###

# length = pd.Series(np.array([0.5, 0.75, 1.0, 1.25, 1.5]))
# t_ten = pd.Series(np.array([14.2, 17.3, 20.1, 22.5, 24.6]))
# experiment = pd.Series(np.array(['A', 'B', 'C', 'D', 'E']))

# data = pd.concat([experiment, length, t_ten], axis='columns')

# data.columns = ['Experiment', 'Length', 'T_ten']

# # data = pd.DataFrame(np.array([length, t_ten]).T, index=experiment)

# print(data)

# # Part 1
# data.set_index('Experiment', inplace=True, drop=True)
# print(data)

# # Part 2
# data['ave_time'] = data['T_ten'] / 10
# print(data)

# # Part 3
# data['theoretical'] = 2 * np.pi * np.sqrt(data['Length'] / 9.8)
# print(data)

# # Part 4
# data['per_error'] = 100 * (data['ave_time'] - data['theoretical']) / data['theoretical']
# print(data)

# # Part 5
# print(data.index[data['per_error'].abs().argmax()])





### --- Activity 3 --- ###

# # Part 1
# df = pd.read_csv('Sales.csv')

# # Part 2
# print(df.head(10))

# # Part 3 
# print(df.info())

# # Part 4
# print(df['Total_Revenue'].sum())

# # Part 5
# print(df.groupby('Category')['Total_Revenue'].sum().sort_values())

# # Part 6
# df_prod = df.groupby('Product_Name')[['Total_Revenue', 'Quantity']].sum()
# print(df_prod.sort_values('Total_Revenue'))
# print(df_prod.sort_values('Quantity'))



### --- Activity 4

iris = pd.read_csv('Iris_dirty.csv')

print(iris.head(20))

iris_no_stem = iris.drop(columns='Stem_length')

iris_no_nan = iris_no_stem.dropna()

dup_mask = iris_no_nan.duplicated('CATID')
print(iris_no_nan[dup_mask])

iris_no_dup = iris_no_nan.drop_duplicates('CATID')
print(iris_no_dup.shape)

print(iris_no_dup.describe())

plt.hist(iris_no_dup['Petal_width'], bins=200)
plt.show()

outlier_mask = (iris_no_dup['Sepal_length'] < 20) & (iris_no_dup['Sepal_width'] < 20) & (iris_no_dup['Petal_width'] < 20)
final_iris = iris_no_dup[outlier_mask]

print(final_iris.shape)

