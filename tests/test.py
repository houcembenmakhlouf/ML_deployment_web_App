import pickle
import json
from classify_account import classify_user
# This file is only for testing

example_users = pickle.load(
    open('example_data/example_data.p', 'rb'))
print(
    example_users['94c383089f0dd9993020276bd01113ecb5935ad860bfa61e6079e7d548577f76'])
print(
    example_users['94c383089f0dd9993020276bd01113ecb5935ad860bfa61e6079e7d548577f76'].keys())


example_users = pickle.load(
    open('example_data/example_users_extended.p', 'rb'))

# print(example_users)
data = open(
    'example_data/example_users_extended.json', 'w')
json.dump(example_users, data, default=str)
data.close()


exit()
# with open('example_data/data.json', 'w') as fp:
#     json.dump(example_users, fp)

# user1 = example_users['94c383089f0dd9993020276bd01113ecb5935ad860bfa61e6079e7d548577f76']

# data = {}
# for user in range(2000):
#     data[user] = user1
# print(len(data))

# print(
#     example_users['94c383089f0dd9993020276bd01113ecb5935ad860bfa61e6079e7d548577f76']["tweets"][0])
# exit()

# start = time.time()
# for user in data:
#     # print(user)
#     (classify_user(data[user]))
#     # print('----')
# end = time.time()
# print(end - start)

# for user in example_users:
#     print(user)
#     print(classify_user(example_users[user]))
#     print('----')
