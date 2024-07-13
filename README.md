# Algorithmic Trading System - Order Handling API

This project involves designing a module for a hypothetical algorithmic trading system. The trading system handles multiple users, each with a suite of strategies. A strategy is an algorithm that buys or sells a select group of stocks based on certain logic. Each strategy can trade a random group of stocks.

## Project Overview

The goal of this project is to design an API that handles order placements for the trading system. The API processes incoming orders based on the following parameters:
- **STRATEGY:** Indicates which strategy the order pertains to.
- **INSTRUMENT:** Specifies the instrument (stock) to be traded.
- **POSITION:** Indicates the action ("BUY" or "SELL").

**Order Rules:**
- A sell cannot take place without a prior buy.
- A strategy cannot re-buy an instrument until it has been sold.
- The API must validate the order based on the user's strategies and existing orders.

## Example Scenario

1. **Users and Strategies:**
   - *Holland Proctor*: 
     - STRATEGY_A: Trades in "BIRLASOFT", "GRASIM", "EICHER".
     - STRATEGY_B: Trades in "MINDA".
   - *Oaklee Wagner*: 
     - STRATEGY_D: Trades in "ACC".

2. **Order Validations:**
   - Order #1: ("STRATEGY_A", "GRASIM", "SELL") - **Invalid** (GRASIM not bought yet).
   - Order #2: ("STRATEGY_B", "MINDA", "BUY") - **Valid** (Holland Proctor).
   - Order #3: ("STRATEGY_D", "INFY", "BUY") - **Invalid** (INFY not traded by any user).
   - Order #4: ("STRATEGY_A", "MINDA", "SELL") - **Valid** (MINDA was bought in Order #2).

## Project Requirements

The system must:
- Track all existing buy orders yet to be sold.
- Maintain permanent records of these buys (via a database/JSON) to ensure resilience to shutdowns/crashes.
- Optionally, maintain a permanent "order log" of past buys and sells.
- Return the status of each order (Rejected/Accepted) via the API.

## Setup Instructions

### Prerequisites
- Python must be installed.

### Directory Structure
- **Jsons:** Contains necessary JSON files for execution.
- **Logs:** Contains logs generated during execution.
- **Scripts:** Contains Python scripts necessary for execution.

### Running the Project
1. **Generate User Profiles:**
   - Run `Generate_User_Profile.py` to create a JSON file of random user profiles in the `Jsons` folder.
   
   ```bash
   python Scripts/Generate_User_Profile.py

2. **Start the API:**
   - Run Order_Handler.py to start the FastAPI server. The API will be hosted on port 8080.

   ```bash
   uvicorn Scripts.Order_Handler:app --host 0.0.0.0 --port 8080

3. **Produce Orders:**
   - Run Order_Producer.py on a different terminal to produce random orders at 1-second intervals and send them to the API.

   ```bash
   python Scripts/Order_Producer.py


### Notes :
- The current implementation of Order_Handler.py only prints the received orders. You need to extend this API to validate and process the orders as per the rules mentioned above.
