import pickle
import time
from classify_account import classify_user

example_users = pickle.load(open('example_data/example_data.json', 'rb'))

# taking the first user and multiply it by 2000 to extend the data
user1 = example_users['94c383089f0dd9993020276bd01113ecb5935ad860bfa61e6079e7d548577f76']
print(len(example_users))
data = {}
for user in range(2000):
    data[user] = user1

# test the extended data
start = time.time()
for user in data:
    print(user)
    (classify_user(data[user]))
    print('----')
end = time.time()
print(end - start)


# push the extended data in new .json or .p fille
example_users_extendeted = open(
    'example_data/example_users_extendeted.p', 'wb')
pickle.dump(data, example_users_extendeted)
example_users_extendeted.close()


# example_users_extendeted = pickle.load(
#     open('example_data/example_users_extendeted.p', 'rb'))
# print(len(example_users_extendeted))
