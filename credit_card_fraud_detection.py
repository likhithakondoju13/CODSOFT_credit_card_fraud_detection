# -*- coding: utf-8 -*-
"""Copy of CREDIT CARD FRAUD  DETECTION

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1g59zFVZdPeoOiyRcQ2tV8FEN0mShYOjZ
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score

# Load the dataset
train_data = pd.read_csv('fraudTrain.csv')
test_data = pd.read_csv('fraudTest.csv')

# Combine train and test data if needed, or use them separately
data = pd.concat([train_data, test_data])

# Separate features and target
X = data.drop(['is_fraud', 'trans_date_trans_time'], axis=1)  # Dropping 'trans_date_trans_time' if not needed
y = data['is_fraud']

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Define preprocessing steps
numeric_features = X.select_dtypes(include=['number'])
categorical_features = X.select_dtypes(include=['category'])

numeric_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='median')),
    ('scaler', StandardScaler())
])

categorical_transformer = Pipeline(steps=[
    ('imputer', SimpleImputer(strategy='constant', fill_value='missing')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
])

preprocessor = ColumnTransformer(
    transformers=[
        ('num', numeric_transformer, numeric_features.columns),
        ('cat', categorical_transformer, categorical_features.columns)
    ])

# Preprocess the data
X_train_preprocessed = preprocessor.fit_transform(X_train)
X_test_preprocessed = preprocessor.transform(X_test)

# Train the model
model = LogisticRegression()
model.fit(X_train_preprocessed, y_train)

# Make predictions
y_pred = model.predict(X_test_preprocessed)

# Evaluate the model
print("Classification Report:\n", classification_report(y_test, y_pred))
print("Confusion Matrix:\n", confusion_matrix(y_test, y_pred))
print("ROC-AUC Score:", roc_auc_score(y_test, y_pred))