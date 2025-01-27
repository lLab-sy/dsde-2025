"""
    ASSIGNMENT 2 (STUDENT VERSION):
    Using pandas to explore Titanic data from Kaggle (titanic_to_student.csv) and answer the questions.
    (Note that the following functions already take the Titanic dataset as a DataFrame, so you don’t need to use read_csv.)

"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split



def Q1(df: pd.DataFrame):
    """
        Problem 1:
            How many rows are there in the "titanic_to_student.csv"?
    """
    return df.shape[0]


def Q2(df: pd.DataFrame):
    '''
        Problem 2:
            Drop unqualified variables
            Drop variables with missing > 50%
            Drop categorical variables with flat values > 70% (variables with the same value in the same column)
            How many columns do we have left?
    '''
    # TODO: Code here
    df = df.loc[:, df.isna().mean() <= 0.5]

    for col in df.select_dtypes(include=['object']).columns:
        if df[col].value_counts(normalize=True).iloc[0] > 0.7:
            df = df.drop(col, axis=1)

    return df.shape[1]


def Q3(df: pd.DataFrame):
    '''
       Problem 3:
            Remove all rows with missing targets (the variable "Survived")
            How many rows do we have left?
    '''
    # TODO: Code here
    df.dropna(subset=['Survived'], inplace=True)
    return df.shape[0]


def Q4(df: pd.DataFrame):
    '''
       Problem 4:
            Handle outliers
            For the variable “Fare”, replace outlier values with the boundary values
            If value < (Q1 - 1.5IQR), replace with (Q1 - 1.5IQR)
            If value > (Q3 + 1.5IQR), replace with (Q3 + 1.5IQR)
            What is the mean of “Fare” after replacing the outliers (round 2 decimal points)?
            Hint: Use function round(_, 2)
    '''
    # TODO: Code here
    fare_df = df['Fare']

    q1 = fare_df.quantile(0.25)
    q3 = fare_df.quantile(0.75)
    iqr = q3-q1

    lower_bound = q1 - 1.5*iqr
    upper_bound = q3 + 1.5*iqr

    fare_df = np.where(
        fare_df < lower_bound, lower_bound, fare_df
    )

    fare_df = np.where(
        fare_df > upper_bound, upper_bound, fare_df
    )

    return round(fare_df.mean(), 2)


def Q5(df: pd.DataFrame):
    '''
       Problem 5:
            Impute missing value
            For number type column, impute missing values with mean
            What is the average (mean) of “Age” after imputing the missing values (round 2 decimal points)?
            Hint: Use function round(_, 2)
    '''
    # TODO: Code here
    mean_age = df['Age'].mean()
    new_age = df['Age'].fillna(mean_age)
    return round(new_age.mean(), 2)


def Q6(df: pd.DataFrame):
    '''
        Problem 6:
            Convert categorical to numeric values
            For the variable “Embarked”, perform the dummy coding.
            What is the average (mean) of “Embarked_Q” after performing dummy coding (round 2 decimal points)?
            Hint: Use function round(_, 2)
    '''
    # TODO: Code here
    dummies = pd.get_dummies(df['Embarked'], prefix='Embarked')
    new_df = pd.concat([df, dummies], axis=1)
    mean_embarked_q = round(new_df['Embarked_Q'].mean(), 2)
    return mean_embarked_q


def Q7(df: pd.DataFrame):
    '''
        Problem 7:
            Split train/test split with stratification using 70%:30% and random seed with 123
            Show a proportion between survived (1) and died (0) in all data sets (total data, train, test)
            What is the proportion of survivors (survived = 1) in the training data (round 2 decimal points)?
            Hint: Use function round(_, 2), and train_test_split() from sklearn.model_selection, 
            Don't forget to impute missing values with mean.
    '''
    # TODO: Code here
    # mode_sur = 1.0 if df['Survived'].mean() > 0.5 else 0
    mode_sur = df['Survived'].dropna().mean()
    new_df = df
    new_df['Survived'] = df['Survived'].fillna(mode_sur)

    X = new_df.drop('Survived', axis=1)  # Features
    y = new_df['Survived']               # Target variable

    # Perform stratified train-test split
    _, _, y_train, _ = train_test_split(
        X, y, test_size=0.3, random_state=123, stratify=y
    )
    train_proportion = (y_train == 1).sum() / len(y_train)
    train_survived_proportion = round(train_proportion, 2)
    return train_survived_proportion
