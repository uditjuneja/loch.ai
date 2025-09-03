# Approach and Assumptions

## Approach
This project consists of a main package - `app` used to organize the main application logic, including database interactions (in-memory), models, and resources. 


## Strategy to Find PnL (Average Price)
The P&L is calculated by calculating the the average price.

1. **Tracking Trades:** All buy and sell trades are recorded with their respective quantities and prices.

2. **Calculating Average Price:** The average price is computed as the weighted average of all executed trades up to the current point.


**Assumptions:**
	- Partial sells reduce the position and do not affect the average price of the remaining position.
	- No transaction costs or fees are considered in the calculation.
