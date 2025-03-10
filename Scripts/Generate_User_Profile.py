from Logs import logInfo, logCritical
import json
import random

#########################################################
#   This file to creates a random set of user profiles  #
#########################################################

logInfo("Generating user profiles.")

# Number of users
USER_COUNT = 3 

# User Details
with open("../Jsons/raw_details.json") as f:
    raw_details = json.load(f)

# Generating random Strategies along with Instruments
user_profiles = {}
strategy_suite = {}
for s in raw_details['STRATEGIES']:
    strategy_suite[s] = []
    for i in range(random.randint(1,10)):
        while True:
            stock = raw_details["INSTRUMENTS"][random.randint(0,len(raw_details["INSTRUMENTS"]))-1]
            if stock not in strategy_suite[s]:
                strategy_suite[s].append(stock)
                break

# As per the user count specified earlier, generating user profiles
for i in range(USER_COUNT):
    while True:
        user = raw_details["USERS"][random.randint(0,len(raw_details["USERS"]))-1]
        if user not in user_profiles:
            user_profiles[user] = {}
            for j in range(random.randint(1,7)):
                while True:
                    strategy = raw_details["STRATEGIES"][random.randint(0,len(raw_details["STRATEGIES"]))-1]
                    if strategy not in user_profiles[user]:
                        user_profiles[user][strategy] = strategy_suite[strategy]
                        break
            break

# Making JSON of User Profile
with open("../Jsons/user_profile.json",'w') as f:
    json.dump(user_profiles,f,indent=4)

logInfo("User profiles generated.")