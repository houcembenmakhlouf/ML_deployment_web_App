import pickle
from scholarmetrics import hindex
from collections import Counter
import numpy as np
from statistics import mean, median
import math
from sklearn.preprocessing import MinMaxScaler
import os

scaler = MinMaxScaler()
scaler.fit([[-1.785450489125143], [-4.9]])

attributes_path = os.path.join(os.path.dirname(__file__), 'attributes.p')
classifiers_path = os.path.join(
    os.path.dirname(__file__), 'cluser_classifiers_6.p')

attributes = pickle.load(open(attributes_path, 'rb'))
classifiers = pickle.load(open(classifiers_path, 'rb'))
cluster_descriptions = {1: 'Accounts that are software automated, meaning that there is a computer behind every account controlling when the account posts tweets. Tweets from accounts in this cluster have been seen and liked by other users on Twitter. The accounts in this cluster have a low posting intensity which means that the accounts have been inactive over time. The accounts in this cluster show same characteristics as social spambots used for specific purposes and campaigns.',
                        2: 'Accounts that post tweets in non-automatic patterns and get spread of the published tweets. The accounts in this cluster are most likely genuine and human accounts.',
                        3: 'Accounts in this cluster are software automated, meaning that there is not a human being, but a computer, that decides when this account is posting tweets. Furthermore, tweets posted by accounts in this cluster are being spread by other accounts. Accounts in this cluster show similarities to accounts used in influence operations.',
                        4: 'Accounts getting no confirmation or spread at all i.e., they are tweeting for themselves. No other accounts are interacting with accounts in this cluster in the term of sharing or liking their tweets. Accounts in this cluster show similarities to accounts used in influence operations.',
                        5: 'Accounts getting no confirmation at all, but other accounts are interacting with accounts in this cluster by liking their tweets. Accounts in this cluster show similarities to accounts used in influence operations.',
                        6: 'Accounts that reply to other accounts to a high extent. 75 % of the own tweets are replies to other accounts meaning that they these accounts are focused on interacting with other accounts. The accounts in the cluster are relatively young, post tweets in a non-automatic pattern, and show similar characteristics to accounts showing hateful behavior.'}


def calculate_attributes(user):
    user_data = user['user_data']
    tweets = user['tweets']

    if len(tweets) <= 1:
        return ''

    weekday_dist = [0] * 7
    hour_dist = [0] * 24
    minute_dist = [0] * 60
    second_dist = [0] * 60

    weekdays = []
    hour_vs_day = np.zeros((24, 7))
    minute_vs_hour = np.zeros((60, 24))
    second_vs_minute = np.zeros((60, 60))

    retweets_given = 0
    tweets_with_hashtag = 0
    replies_own = 0
    own_tweets_analysed = 1
    number_of_tweets_analysed = 1
    retweets_gotten = []
    likes_gotten = []
    own_tweets_w_mentions = 0
    retweeted_users = []
    hashtags_all = []
    own_tweets_w_hashtags = 0
    hashtags_own = []
    languages = []
    burst_times = []

    for tweet in tweets:
        number_of_tweets_analysed += 1
        weekday_dist[tweet['created_at'].weekday()] += 1
        hour_dist[tweet['created_at'].hour] += 1
        minute_dist[tweet['created_at'].minute] += 1
        second_dist[tweet['created_at'].second] += 1

        weekday = tweet['created_at'].weekday()
        hour = tweet['created_at'].hour
        minute = tweet['created_at'].minute
        second = tweet['created_at'].second

        hour_vs_day[hour, weekday] += 1
        minute_vs_hour[minute, hour] += 1
        second_vs_minute[second, minute] += 1
        weekdays.append(weekday)

        # Bursts
        burst_times.append(tweet['created_at'].timestamp())

        if tweet['lang'] != 'und':
            languages.append(tweet['lang'])

        # RETWEETS
        if 'retweeted_status' in list(tweet.keys()):
            retweets_given += 1
            retweeted_users.append(
                tweet['retweeted_status']['user']['screen_name'])

        # OWN TWEETS
        else:
            replies_own += 1 if tweet['in_reply_to_status_id'] != None else 0

            own_tweets_w_mentions += 1 if tweet['in_reply_to_status_id'] == None and len(
                tweet['entities']['user_mentions']) != 0 else 0

            own_tweets_w_hashtags += 1 if len(
                tweet['entities']['hashtags']) != 0 else 0

            own_tweets_analysed += 1
            retweets_gotten.append(tweet['retweet_count'])
            likes_gotten.append(tweet['favorite_count'])

            for hashtag in tweet['entities']['hashtags']:
                hashtags_own.append(hashtag['text'])

        for hashtag in tweet['entities']['hashtags']:
            hashtags_all.append(hashtag['text'])

        if len(tweet['entities']['hashtags']):
            tweets_with_hashtag += 1

    # Burst
    bins = np.linspace(min(burst_times), max(burst_times), 11)

    dt_bin = bins[1] - bins[0]

    burst_dist = list(np.digitize(np.array(burst_times), bins))[1:]
    bin_counter = Counter(burst_dist)
    for i in range(1, 11):
        if i not in bin_counter:
            bin_counter[i] = 0

    bursts_d = [round(bin_counter[i] / dt_bin * 60 * 60 * 24, 4)
                for i in bin_counter]

    burst = max(bursts_d)-median(bursts_d)
    if math.isnan(burst):
        burst = 0
    if len(burst_times) == 1:
        burst = 0

    # Anonymous FEATURES
    if user_data['verified']:
        anonymity = 0
    else:
        anonymity = 3 - (1 if user_data['url'] != None else 0) - \
            (1 if user_data['location'] != '' else 0)

    # standard name attribute
    standard_name = 1 if len(user) >= 8 and user[-8:].isnumeric() else 0

    # Popularity FEATURES
    popularity_feature = user_data['followers_count']

    # Posting intensity feature
    posting_intensity = user_data['statuses_count'] / \
        float(((user['crawled_at'] - user_data['created_at']).days) + 1)

    # Confirmation features
    confirmation_max = max(likes_gotten) if len(likes_gotten) > 0 else 0
    confirmation_mean = mean(likes_gotten) if len(likes_gotten) > 0 else 0
    confirmation_h = round(hindex(likes_gotten) /
                           len(likes_gotten), 4) if len(likes_gotten) > 0 else 0

    # Spread features
    spread_max = max(retweets_gotten) if len(retweets_gotten) > 0 else 0
    spread_mean = mean(retweets_gotten) if len(retweets_gotten) > 0 else 0
    spread_h = round(hindex(retweets_gotten) / len(retweets_gotten),
                     4) if len(retweets_gotten) > 0 else 0

    # Interaction (with other accounts) features
    interaction_hashtags = own_tweets_w_hashtags / float(own_tweets_analysed)
    interaction_replies = replies_own / float(own_tweets_analysed)
    interaction_mentions = own_tweets_w_mentions / float(own_tweets_analysed)

    # spreader features
    spreader = round(retweets_given / float(number_of_tweets_analysed), 4)

    # automatic posting features
    automatic_posting_seconds = np.var(
        [float(i) / sum(second_dist) for i in second_dist])
    automatic_posting_minutes = np.var(
        [float(i) / sum(minute_dist) for i in minute_dist])
    automatic_posting_hours = np.var(
        [float(i) / sum(hour_dist) for i in hour_dist])
    automatic_posting_days = np.var(
        [float(i) / sum(weekday_dist) for i in weekday_dist])

    # Language variation FEATURES
    if len(languages) > 0:
        language_variation_feature = len(set(languages))
    else:
        language_variation_feature = 0

    attributes = {'anonymity': anonymity,
                  'popularity': math.log10(popularity_feature) if popularity_feature != 0 else -10,
                  'confirmation_max': math.log10(confirmation_max) if confirmation_max != 0 else -10,
                  'confirmation_mean': math.log10(confirmation_mean) if confirmation_mean != 0 else -10,
                  'confirmation_h': confirmation_h,
                  'spread_max': math.log10(spread_max) if spread_max != 0 else -10,
                  'spread_mean': math.log10(spread_mean) if spread_mean != 0 else -10,
                  'spread_h': spread_h,
                  'interaction_mentions': interaction_mentions,
                  'interaction_replies': interaction_replies,
                  'interaction_hashtags': interaction_hashtags,
                  'spreader': spreader,
                  'posting_intensity': posting_intensity,
                  'posting_automation_seconds': math.log10(automatic_posting_seconds),
                  'posting_automation_minutes': math.log10(automatic_posting_minutes),
                  'posting_automation_hours': math.log10(automatic_posting_hours),
                  'posting_automation_days': math.log10(automatic_posting_days),

                  'language_variation': language_variation_feature,
                  'age': (user['crawled_at'] - user_data['created_at']).days,

                  'standard_name': standard_name,
                  'burst': burst,
                  }

    return {'_id': user,
            'created_at': user_data['created_at'],
            'attributes': attributes}


def classify_from_attributes(user_data):
    data = [user_data['attributes'][attribute] for attribute in attributes]
    # classifier is a RandomForestClassifier
    values = [classifier.predict_proba([data])[0][1]
              for classifier in classifiers]
    prediction = values.index(max(values))+1
    return {'prediction': prediction,
            'description': cluster_descriptions[prediction]}


def classify_user(user_data):
    user_attributes = calculate_attributes(user_data)
    user_classification = classify_from_attributes(user_attributes)
    return user_classification
