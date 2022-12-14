# Project: Machine learning model deployment for web App
<p align="center">
<img src="https://user-images.githubusercontent.com/45092804/197417249-798510f5-60f3-4020-ae5b-e903eb4a473a.png" width="400" />
</p>

## Problem definition
The deployment of machine learning models is the process of making models available in production where web applications, enterprise software and APIs can consume the trained model by providing new data points and generating predictions. Our main task in this project consists of integrating a tweets classification model into a production environment which can take in an input and return an output that can be used in making practical decisions to help the user figure out if the tweets are coming from a robot. Our project come with the importance of giving people more insight about the tweeted data.

## Requirements and installations

After getting the repository of the project, we should create a python environment so that we can install all packages we need for this project which are going to be installed as dependencies in our app, more precisely in package.json. To create our virtual environment, we can execute the command line after specifying the path where we want to create our environment.
```
python3 -m venv /path/to/new/virtual/environment
```
To install these requirements, we need to pass the command line
```
pip install -r requirements.txt
```
To launch the project, we should:

•Activate the environment via
```
 venv\scripts\activate
```
• Launch the server via
```
python .\main.py
```
• Go under tests and begin sending requests
```
$ cd tests
$ python .\send_requests.py
```
## Project overview
### general overview
In our project there are mainly two big parts:
• The model part: where the algorithm of our model is defined with its different features and parameters. The model is already trained over a set of data and we can use it directly. The Algorithm of this part is found under the file classify_account.py
• The deployment part: This part is main purpose of this project and it consists of building a REST API using Flask. This python framework will allow us to create a deployment component that will interact with our machine learning model and the user. It will take that input data given as an external file from the user, process it and then pass it to model to get the predicted data as an output which will be visualized to the user. This part is developed in the file “main.py”.
The figure 2 shows the general circulation of the information in our project.

<p align="center">
<img src="https://user-images.githubusercontent.com/45092804/197418937-9348ded6-748e-4c4b-9417-3cd92e2cd268.png" width="400" />
</p>


### input format

Data type and formats are one of the essential parts when working on a machine learning algorithm. The Data should be clean as possible to minimize error; missing values should be filled out if there is any. Data should be reduced for proper data handling. The data type is very important to precise so that we don’t get any errors of compatibilities with the model.
the general structure of our data is as follows:

```
Dict{"user_key1":{ 'user_data':..., 'tweets':..., 'crawled_at':...}, "user_key2":{}...}
```
### output format

the model is going to classify the given users into one of 6 classes. For each user, we get predicted class and the description of that class.
```
{'prediction': 4, 'description': 'Accounts getting no confirmation or spread at all i.e., they are tweeting for themselves. No other accounts are interacting with accounts in this cluster in the term of sharing or liking their tweets. Accounts in this cluster show similarities to accounts used in influence operations.'}
```
### testing

A reduced version of the entire data is used to test the functionality of the algorithm. After the testing part, the data set was multiplied into 1000 and 2000 users to test further the performance. To simplify the work, we took the first instance of data set and we applied the multiplication process. The table below shows the time needed to get the predicted results taking into consideration the data size:

<center>
 
| Data set size (number of users)  | 5 | 1000 | 2000 |
| ------------- | ------------- | ------------- | ------------- |
| Time needed to get results (Seconds) | 0.04590916  | 7.29847478 | 16.06111311 |
 
</center>

To further test the asynchronous behaviour another file “send_requests.py” is added where we can pass a predefined number of requests in the same time. These requests will be treated one by one. The table below shows the time needed in seconds to get all the predicted results when passing a predefined number of requests using the original data set that was provided and an extended data set with 2000 users.

<center>
 
| Number of requests  | 5 | 10 | 15 |
| ------------- | ------------- | ------------- | ------------- |
| Original data | 5.44167089  | 10.82522678 | 17.76469802 |
| Extended data | 125.926930  | 279.5530014 | 386.4041688 |
 
</center>

### two ways to pass the data

• Using Curl which is used in command lines or scripts to transfer data. Here below an example of command is presented. To make this command line work I used “BufferedReader” which reads data from the object and kept in an internal buffer.
```
curl -i -X POST -H 'Content-Type: application/json' -F 'data=@/example_data.p' http://localhost:5000/process
```
• Using the terminal of the project when compiling the “send_requests.py” file. This method is more reliable in our case because more details and tests can be done in the future. Also, we can modify certain parameters like in our case, we wanted to test the time needed if we pass the request many times.

## Perspectives and conclusions

The project dealt with the subject of deployment of a machine learning model which classifies tweets based on their credibility. I have worked on data types, especially how to pre-process the data and make it ready for the processing phase. I understood better the asynchronous behaviour and I knew better how a flask Rest API works. As a perspective, I thought of building a user interface which I integrated a reduced version of it in the “main.py” component because I think it is always more user-friendly.



# More details about Multiclass bot classification

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

