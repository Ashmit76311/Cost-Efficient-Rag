# Machine Learning

Machine learning is a branch of artificial intelligence that enables systems to learn patterns from data and make predictions without being explicitly programmed. It has applications in image recognition, natural language processing, recommendation systems, fraud detection, and many more fields.

## Types of Machine Learning

**Supervised Learning** uses labeled training data where each input has a corresponding target output. The model learns a mapping from inputs to outputs. It is divided into classification (predicting discrete labels like spam/not spam) and regression (predicting continuous values like house prices). Common algorithms include linear regression, logistic regression, decision trees, random forests, support vector machines (SVM), and k-nearest neighbors (KNN).

**Unsupervised Learning** works with unlabeled data to find hidden patterns or structure. Clustering algorithms like K-Means, DBSCAN, and hierarchical clustering group similar data points together. Dimensionality reduction techniques like PCA (Principal Component Analysis) and t-SNE reduce the number of features while preserving important information. Unsupervised learning is used for customer segmentation, anomaly detection, and data exploration.

**Reinforcement Learning** involves an agent learning to make decisions by interacting with an environment. The agent receives rewards or penalties based on its actions and learns a policy that maximizes cumulative reward. Applications include game playing (AlphaGo), robotics, and autonomous driving.

## Bias-Variance Tradeoff

The bias-variance tradeoff is a fundamental concept in machine learning. Bias is the error from overly simplistic assumptions in the model (underfitting), while variance is the error from sensitivity to fluctuations in the training data (overfitting). A model with high bias oversimplifies and performs poorly on both training and test data. A model with high variance fits training data too closely and generalizes poorly to new data.

The goal is to find the sweet spot that minimizes total error (bias^2 + variance + irreducible error). Techniques to manage this tradeoff include cross-validation, regularization, and ensemble methods.

## Evaluation Metrics

For classification: accuracy, precision, recall, F1-score, ROC-AUC, and confusion matrix. Precision measures the fraction of positive predictions that are correct. Recall measures the fraction of actual positives that are correctly identified. F1-score is the harmonic mean of precision and recall.

For regression: Mean Squared Error (MSE), Root Mean Squared Error (RMSE), Mean Absolute Error (MAE), and R-squared. R-squared indicates the proportion of variance in the target variable explained by the model.

## Feature Engineering

Feature engineering is the process of creating new features or transforming existing ones to improve model performance. Techniques include one-hot encoding for categorical variables, normalization/standardization for numerical features, handling missing values through imputation, and creating interaction features. Good feature engineering often matters more than choosing a sophisticated algorithm.

## Cross-Validation

Cross-validation is a technique for assessing how well a model generalizes to unseen data. K-fold cross-validation splits data into k folds, trains on k-1 folds, and tests on the remaining fold, repeating k times. Stratified k-fold ensures each fold has approximately the same distribution of target classes. Cross-validation gives a more reliable estimate of model performance than a single train-test split.

## Regularization

Regularization prevents overfitting by adding a penalty term to the loss function. L1 regularization (Lasso) adds the sum of absolute values of weights, promoting sparsity. L2 regularization (Ridge) adds the sum of squared weights, preventing any single weight from becoming too large. Elastic Net combines both L1 and L2 penalties. The regularization strength is controlled by a hyperparameter (usually called lambda or alpha).
