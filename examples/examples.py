# IBCP Examples
# This file contains examples of how to use the IBCP library

import ibcp

# Create a REST client
api = ibcp.REST()
# default parameters: url="https://localhost:5000", ssl=False
# SSL warnings can be suppressed by setting up a SSL certificate, or type "export PYTHONWARNINGS="ignore:Unverified HTTPS request" in a shell

# Example: Get historical data
# bars = api.get_bars("TSLA")["data"]
# print(bars)

# Example: Submit orders
# list_of_orders = [
#     {
#         "conid": api.get_conid("TSLA"),
#         "orderType": "MKT",
#         "side": "BUY",
#         "quantity": 6,
#         "tif": "GTC",
#     }
# ]
# result = api.submit_orders(list_of_orders)
# print(result)

# Example: Modify order
# order = {
#     "conid": api.get_conid("TSLA"),
#     "orderType": "MKT",
#     "side": "BUY",
#     "quantity": 7,
#     "tif": "GTC",
# }
# result = api.modify_order(1258176647, order)
# print(result)

# Example: Get order status
# order_status = api.get_order(1258176647)
# print(order_status)

# Example: Get live orders
# live_orders = api.get_live_orders()
# print(live_orders)

print("IBCP examples loaded successfully!")
print("Uncomment the examples above to run them.")
