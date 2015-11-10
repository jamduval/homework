# Class 14 Homework, Yelp Review Text

import pandas as pd
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import numpy as np

%matplotlib inline
import matplotlib.pyplot as plt
plt.rcParams['figure.figsize'] = (8, 6)
plt.rcParams['font.size'] = 14

# (1) Read the yelp.csv into a dataframe.

fname = r'f:\Git_Repositories\DAT-DC-9\data\yelp.csv'
stars = pd.read_table(fname, sep=',')
stars.head()
stars.shape

# (2) Create a dataframe with only 5-star and 1-star reviews.

stars = stars[(stars.stars == 5) | (stars.stars == 1)]

# Check that only 1 and 5 star reviews remain.
stars.shape
stars.groupby('stars').stars.value_counts()

# (3) Split the new DataFrame into training and testing sets,
#     using the review text as the only feature and the star 
#     rating as the response.

# Assign my feature and response variables.
X = stars.text
y = stars.stars

X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=1)

#Check to make sure the shape of the data is as we expect.
print(X_train.shape)
print(X_test.shape)

# (4) Use CountVectorizer to create document-term matrices 
#     from X_train and X_test.

vect = CountVectorizer() # Instantiate the model
vect.fit(X_train)
X_train_tokens = vect.get_feature_names()
X_train_dtm = vect.transform(X_train)
X_test_dtm = vect.transform(X_test)

# Check to make sure that the shape of the data is as we expect.
print(X_train_dtm)
print(X_test_dtm)
print(X_train_dtm.shape)
print(X_test_dtm.shape)
print(X_train_tokens[-50:]) #Looks at the last 50 words.

# (5) Use Naive Bayes to predict the star rating for reviews in the
#     testing set, and calculate the accuracy.

#Instantiate the NB model, note that if this was continuous data
#then we would use the GuassianNB model.
nb = MultinomialNB() 
nb.fit(X_train_dtm, y_train)

# Make the class predictions based on our testing data
y_pred_class = nb.predict(X_test_dtm)

print(y_pred_class.shape)

# Calculate the accuracy score by printing the accuracy of the
# class predictions.

print(metrics.accuracy_score(y_test, y_pred_class))

# (6) Calculate the AUC (area under the curve)

#Need to map the values to 0 and 1 so roc_auc_score does not
#get confused.
y_test_ind = y_test.map({1:0, 5:1})
y_pred_prob = nb.predict_proba(X_test_dtm)[:, 1]
print(y_pred_prob) #look at some of the predicted probabilities.
print(metrics.roc_auc_score(y_test_ind, y_pred_prob))

# (7) Plot the ROC curve.

fpr, tpr, thresholds = metrics.roc_curve(y_test_ind, y_pred_prob)
plt.plot(fpr, tpr)
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.0])
plt.title('Measuring the Performance of the Model Using the ROC Curve')
plt.xlabel('False positive rate (1 - specificity)')
plt.ylabel('True positive rate (sensitivity)')

# (8) Print the confusion matrix, and calculate the sensitivity 
#     and specificity. Comment on the results

confusion = metrics.confusion_matrix(y_test,y_pred_class)
print(metrics.confusion_matrix(y_test, y_pred_class))

TP = confusion[1][1] #True positives, we predicted a 5-star review correctly
TN = confusion[0][0] #True negatives, we predicted a 1-star review correctly
FP = confusion[0][1] #False positives, we incorrectly predicted a true 5-star review
FN = confusion[1][0] #False negatives, we incorrectly predicted a true 1-star review

# Sensitivity
print(TP / float(TP + FN))

# A sensitivity of 0.97 indicates that we correctly identify 
# 97 percent of the true 5-star reviews.

# Specificity
print(TN / float(TN + FP))

# A specificity of 0.68 indicates that we correctly identify
# 68 percent of the true 1-star reviews.

# The above results seem to indicate that our model is more inclined
# to denote a review as positive than negative, which could potentially
# lead us to a lack of information on how places could improve.

# (9) Browse through the review text for some of the false positives 
#     and false negatives. Based on your knowledge of how Naive Bayes works, 
#     do you have any theories about why the model is incorrectly classifying 
#     these reviews?

# Let's first look at the false negatives, so our test value was
# actually a one-star review, but we predicted it to be a 5-star review.
X_test[y_test < y_pred_class]

X_test[9125] #I changed this at will to look at false negatives.

# Let's then look at the false positives, so our test value was 
# a five-star review, but we prodicted it to be a one-star review.
X_test[y_test > y_pred_class]

X_test[241] #I changed these at will to look at false positives.
X_test[4034]

# My guess as to why the Naive Bayes model is incorrectly classifying these
# reviews is that, in the case of the false positives, their reviews are set up
# as "it would be bad if the place did this, but they did not!" Essentially,
# these reviewers are using "negative" words in a "positive review, so our model
# might be more often associating words such as "not" and "sad" with 1-star 
# reviews, but these reviewers are using them in good reviews. So as they describe
# how each potential negative aspect is good at the place they are reviewing,
# it is causing our model to incorrectly classify the review. The same (but reverse)
# logic applies to the reviews that are truly one-star reviews but the model 
# predicts them to be 5-star reviews.

# (10) Let's pretend that you want to balance sensitivity and specificity. 
# You can achieve this by changing the threshold for predicting a 5-star 
# review. What threshold approximately balances sensitivity and specificity?

# This shows us that the probabilities are typically either 1 or 0
plt.hist(y_pred_prob)
plt.xlim(0, 1)
plt.title('Probability of a Review Being Classified Correctly')
plt.xlabel('Predicted probability of reviews')
plt.ylabel('Frequency')

y_pred_class2 = np.where(y_pred_prob > 0.998, 5, 1)
confusion2 = metrics.confusion_matrix(y_test, y_pred_class2)
print(confusion)
print(confusion2)

TP2 = confusion2[1][1] #True positives, we predicted a 5-star review correctly
TN2 = confusion2[0][0] #True negatives, we predicted a 1-star review correctly
FP2 = confusion2[0][1] #False positives, we incorrectly predicted a true 5-star review
FN2 = confusion2[1][0] #False negatives, we incorrectly predicted a true 1-star review

# Sensitivity
print(TP2 / float(TP2 + FN2))

# Specificity
print(TN2 / float(TN2 + FP2))

# The above shows that to balance sensitivity and specificity, we need to limit
# our threshold to 0.998. What this means is that if we increase our threshold for
# predicting a true five-star review to 0.998, then we can increase the specificity 
# (the ability to correctly identify the one-star reviews) to match the level 
# of our sensitivity (which has now fallen as a tradeoff of increasing the specificity).

# (11) Let's see how well Naive Bayes performs when all reviews are included, 
#      rather than just 1-star and 5-star reviews:

# (a) Define X and y using the original DataFrame from step 1. (y should 
#     contain 5 different classes.)

fname = r'f:\Git_Repositories\DAT-DC-9\data\yelp.csv'
stars = pd.read_table(fname, sep=',')
stars.head()
stars.shape
stars.groupby('stars').stars.value_counts()

X = stars.text
y = stars.stars

# (b) Split the data into training and testing sets.

X_train, X_test, y_train, y_test = train_test_split(X,y,random_state=1)

# (c) Calculate the testing accuracy of a Naive Bayes model.

vect = CountVectorizer() # Instantiate the model
vect.fit(X_train)
X_train_tokens = vect.get_feature_names()
X_train_dtm = vect.transform(X_train)
X_test_dtm = vect.transform(X_test)
nb = MultinomialNB() 
nb.fit(X_train_dtm, y_train)
y_pred_class = nb.predict(X_test_dtm)
print(metrics.accuracy_score(y_test, y_pred_class))

# (d) Compare the testing accuracy with the null accuracy.

# We calculate the null accuracy by finding the number of true 5-star positives.
five_star = y_test.value_counts().head(0)[5]

# Our five star review is 832.

y_null = five_star / len(y_test)

print(y_null)

# We see that the null accuracy is 0.333 while the testing accuracy is 0.47.

# (e) Print the confusion matrix.

print(metrics.confusion_matrix(y_test, y_pred_class))

# (f) Comment on the results.

# The confusion matrix tells us that for the majority of the time, we predict
# the 4 star reviews correctly (as the diagonal represents where we correctly
# made a prediction). This seems kind of messy between the blurred lines of the 
# four and five star reviews, but 47% of the time, we are predicting the correct
# value. 


