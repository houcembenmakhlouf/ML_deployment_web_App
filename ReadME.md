# Project: Machine learning model deployment for web App
<p align="center">
<img src="https://user-images.githubusercontent.com/45092804/197417249-798510f5-60f3-4020-ae5b-e903eb4a473a.png" width="400" />
</p>
# Multiclass bot classification

The multiclass bot classification model is used for classification of Twitter accounts. The model relies on 19 easy-to-explain attributes which have resulet in high explainability regarding what differenciates the different clusters.

## Setup
Start with cloning the repository.
Install the needed Python libraries by executing the follow command from project folder.

>pip3 install -r requirements.txt  

## Usage
Just import and call the neccessary function as is shown in test.py

    import pickle
    from classify_account import classify_user
    
    example_users = pickle.load(open('example_data/example_data.p','rb'))
    for user in example_users:
        print(user)
        print(classify_user(example_users[user]))
        print('----')

which should give outputs such as:

    94c383089f0dd9993020276bd01113ecb5935ad860bfa61e6079e7d548577f76
    {'prediction': 4, 'description': 'Accounts getting no confirmation or spread at all i.e., they are tweeting for themselves. No other accounts are interacting with accounts in this cluster in the term of sharing or liking their tweets. Accounts in this cluster show similarities to accounts used in influence operations.'}
#### Cluster characteristics
The following table describes the different characteristics of each of the clusters. These descriptions are also provided with the output of the function.

| Cluster id         | Characteristics |
|------------------------|-----------------|
| 1 | Accounts that are software automated, meaning that there is a computer behind every account controlling when the account posts tweets. Tweets from accounts in this cluster have been seen and liked by other users on Twitter. The accounts in this cluster have a low posting intensity which means that the accounts have been inactive over time. The accounts in this cluster show same characteristics as social spambots used for specific purposes and campaigns. |
| 2 | Accounts that post tweets in non-automatic patterns and get spread of the published tweets. The accounts in this cluster are most likely genuine and human accounts. |
| 3 | Accounts in this cluster are software automated, meaning that there is not a human being, but a computer, that decides when this account is posting tweets. Furthermore, tweets posted by accounts in this cluster are being spread by other accounts. Accounts in this cluster show similarities to accounts used in influence operations. |
| 4 | Accounts getting no confirmation or spread at all i.e., they are tweeting for themselves. No other accounts are interacting with accounts in this cluster in the term of sharing or liking their tweets. Accounts in this cluster show similarities to accounts used in influence operations. |
| 5 | Accounts similar to cluster 4, but other accounts are interacting with accounts in this cluster by liking their tweets. Accounts in this cluster show similarities to accounts used in influence operations. |
| 6 | Accounts that reply to other accounts to a high extent. 75 \% of the own tweets are replies to other accounts meaning that they these accounts are focused on interacting with other accounts. The accounts in the cluster are relatively young, post tweets in a non-automatic pattern, and show similar characteristics to accounts showing hateful behavior. |

## Data
To classify an account, the following data is needed:
* Account meta data provided from Twitter's API
* A set of tweets from the account (>50 tweets is preferable) 
* Date the account and tweets were crawled

#### Data format
The account data should be provided to the function as a Python dict with the following keys:

| Key         | Data format | Content |
|------------------------|-----------------|------------|
| user_data | dict | holding all user's metadata provided with the Twitter API |
| tweets | list | a list of dicts where every dict corresponds to a status object on the same form as from the Twitter API | 
| crawled_at | datetime | datetime object of the time the account was crawled|

#### Example file
In the example_data directory, a Python pickled file of a dict holding example data for five different accounts can be found.

