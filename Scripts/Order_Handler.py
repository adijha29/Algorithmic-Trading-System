from fastapi import FastAPI
import requests
import json
from time import sleep
from Logs import logInfo
from Logs import recordLogInfo

#############################################################
#           The API that handles incoming orders.           #
#############################################################

# Initializing FastAPI
app = FastAPI()

# Maintaining User Based on Strategis
with open("../Jsons/raw_details.json") as f:
    raw_details = json.load(f)

# Inserting all Strategies in the dictionary
userBasedOnStrategy = {}
strategywiseStock = {}
userWiseStockPurchased = {}

# To maintain the stocks count
stockCount = {}

# To maintain the record of users along with the strategy and stock
userStockRecord = {}
for strat in raw_details["STRATEGIES"]:
    userBasedOnStrategy[strat] = []
    stockCount[strat] = {}

# Loading Generated Profiles
with open("../Jsons/user_profile.json") as f:
    user_profiles = json.load(f)


# Algorithm for Order Handler
for user in user_profiles:
    userWiseStockPurchased[user] = {}        
    for strat in user_profiles[user]:
        userWiseStockPurchased[user][strat] = {}        
        userBasedOnStrategy[strat].append(user)
        if strat not in strategywiseStock.keys():
            strategywiseStock[strat] = user_profiles[user][strat]
        for stocks in user_profiles[user][strat]:
            userWiseStockPurchased[user][strat][stocks] = False    

# Initializing the Stock Count of every strategy to 0;
for strat in strategywiseStock:
    for stock in strategywiseStock[strat]:
        stockCount[strat][stock] = 0


# Debugging Purpose
# for i in strategywiseStock:
#     print(i," :: ",strategywiseStock[i])
# for i in userBasedOnStrategy:
#     print(i," :: ",userBasedOnStrategy[i])
# for i in stockCount:
#     print(i," :: ",stockCount[i])


def canOrder(order : dict):
    # Fetching details from dictionary
    strat = order["STRATEGY"]
    stock = order["INSTRUMENT"]
    position = order["POSITION"]

    # Checks for Order Validation
    # 1. Check if any user is available for the particular strategy
    if len(userBasedOnStrategy[strat]) == 0:
        return {
            "Order Status" : "Failed",
            "Reason" : f"No user in {strat}"
        }
    # 2. Check if the stock is present in the startegy
    if stock not in strategywiseStock[strat]:
        return {
            "Order Status" : "Failed",
            "Reason" : f"{stock} not found in {strat}"
        }
    
    # 3. Check if the user has already purchased the stock
    if position == "BUY":
        # If no valid user is available for purchasing
        if stockCount[strat][stock] == len(userBasedOnStrategy[strat]):
            return {
                "Order Status" : "Failed",
                "message":"No user available"
            }
        # User Available - Order can be accepted
        else:
            stockCount[strat][stock] = stockCount[strat][stock] + 1
            index = stockCount[strat][stock] - 1
            userWiseStockPurchased[userBasedOnStrategy[strat][index]][strat][stock] = True
            recordLogInfo(
                {
                    "User": userBasedOnStrategy[strat][index],
                    "Strategy": strat,
                    "Stock": stock,
                    "Position":position
                }
            )
            return {
                "Order Status" : "Accepted",
                "message":"Purchased"
            }
    # 4. Check if the user has already sold the stock
    else: 
        # If no valid user is available for selling
        if stockCount[strat][stock] == 0:
            return {
                "Order Status" : "Failed",
                "message":"No buy, direct sell"
            }
        # User Available - Order can be accepted
        else:
            stockCount[strat][stock] = stockCount[strat][stock] - 1
            index = stockCount[strat][stock]
            userWiseStockPurchased[userBasedOnStrategy[strat][index]][strat][stock] = False
            recordLogInfo(
                {
                    "User": userBasedOnStrategy[strat][index],
                    "Strategy": strat,
                    "Stock": stock,
                    "Position":position
                }
            )
            return {
                "Order Status" : "Accepted",
                "message":"Selled"
            }
    
    return {
        "Order Status" : "Failed",
        "Reason" : "Invalid Order"
    }

# Maintains order history
order_history = []

# Root
@app.get("/")
async def root():
    return {"message":user_profiles}

# On API Hit - /create_order - Processing payload
@app.post("/create_order")
async def process_payload(payload: dict):
    # Fetching values of strategy, stock and position from payload
    strategy = payload['STRATEGY']
    stock = payload['INSTRUMENT']
    position = payload['POSITION']

    # Processing Order Request
    res =  canOrder(payload)

    # Logging the Order Results
    order_history.append([res["Order Status"],strategy,stock,position])

    return res