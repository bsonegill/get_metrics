from flask import Flask, send_file, jsonify
import pandas as pd
import datetime
import os

# Start Flask and set config
app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

cwd = os.getcwd()
data_dir = cwd + '/data'

# Create DF's from files
commissions_df = pd.read_csv(data_dir + '/commissions.csv')
orders_df = pd.read_csv(data_dir + '/orders.csv')
order_lines_df = pd.read_csv(data_dir + '/order_lines.csv')
products_df = pd.read_csv(data_dir + '/products.csv')
product_promotions_df = pd.read_csv(data_dir + '/product_promotions.csv')
promotions_df = pd.read_csv(data_dir + '/promotions.csv')

def average(numbers):
    if len(numbers) == 0:
        return 0
    return (sum(numbers) / len(numbers))

@app.route("/get_metrics/<string:date>")
def get_metrics(date):
    # check for correct date format
    date_format = '%Y-%m-%d'
    try:
        date_obj = datetime.datetime.strptime(date, date_format)
    except ValueError:
        return "Incorrect data format, should be YYYY-MM-DD"
    ########################################################################
    # Total number of items sold on that day
        # Corresponding variable to return --> "date_quantity"
    ########################################################################

    # Get DF of orders made on date
    orders_by_date_df = orders_df.set_index("created_at")
    date_orders_df = orders_by_date_df.filter(like=date, axis=0)

    # Check if there is data for date
    if date_orders_df.empty:
        return "No data for {}".format(date)

    # Get list of all orders made on date
    orders_on_date = date_orders_df["id"].tolist()

    # Sort order_lines to only orders made on date
    id_order_lines_df = order_lines_df[order_lines_df['order_id'].isin(orders_on_date)]

    # Get the sum of the quantity column to return
    date_quantity = sum(id_order_lines_df['quantity'].tolist())

    ########################################################################
    # Total number of customers that made an order that day
        # Corresponding variable to return --> "customers_on_date"
    ########################################################################

    customers_on_date = len(set(date_orders_df["customer_id"].tolist()))

    ########################################################################
    # The total amount of discount given that day
        # Corresponding variable to return --> "discount_on_date"

    # The average discount rate applied to the items sold that day (zero excluded)
        # Corresponding variable to return --> "average_discount_on_date"
    ########################################################################

    discount_on_date = 0
    discount_rates_on_date = []
    for index, row in id_order_lines_df.iterrows():
        discount_amount = row["full_price_amount"] - row["discounted_amount"]
        discount_on_date += discount_amount

        discount_rate = row["discount_rate"]
        if discount_rate != 0:
            discount_rates_on_date.append(discount_rate)

    average_discount_on_date = average(discount_rates_on_date)

    ########################################################################
    # The average order total for that day (taken of total_amount)
        # Corresponding variable to return --> "average_order_amount_on_date"
    ########################################################################

    order_amounts = []
    for order in orders_on_date:
        loop_df = id_order_lines_df[id_order_lines_df['order_id'] == order]
        order_amounts.append(sum(loop_df["total_amount"].tolist()))
    average_order_amount_on_date = average(order_amounts)

    ########################################################################
    # The total amount of commissions generated that day (taken of total_amount)
        # Corresponding variable to return --> "total_commissions"

    # The average amount of commissions per order for that day
        # Corresponding variable to return --> "average_commission"

    # The total amount of commissions earned per promotion that day
        # Corresponding variable to return --> "commissions_per_promotion"
    ########################################################################

    # Get DF's of commission rates and vendors on date AND product promotions on date
    date_commission_rate_df = commissions_df[commissions_df["date"] == date]
    date_product_promotions_df = product_promotions_df[product_promotions_df["date"] == date]

    # Get a list of products on promotion that day
    product_promotion_on_date = date_product_promotions_df["product_id"].tolist()

    # Create dictionary to hold the information on promotions and how much commission they generated
    promotions_count = len(promotions_df["id"].tolist())
    promotions = {}

    for i in range(promotions_count):
        key = promotions_df["id"][i]
        promotions[key] = []

    # Get a list of all commissions paid out on date
    commissions = []
    for i in range(len(order_amounts)):
        # Get i-th order amount, id and vendor
        amount = order_amounts[i]
        id = orders_on_date[i]
        row = date_orders_df.loc[date_orders_df['id'] == id]
        vendor = row.iloc[0]["vendor_id"]
        # Get commission rate of that vendor on date
        commission_rate_df = date_commission_rate_df[date_commission_rate_df["vendor_id"] == vendor]
        commission_rate = commission_rate_df.iloc[0]["rate"]
        # Add to list of commission amounts on date
        commissions.append(commission_rate * amount)

        # get DF of all order lines for each order on date
        single_id_order_lines_df = id_order_lines_df[id_order_lines_df["order_id"] == id]

        # Use values from above to find commissions per promotion on date
        order_length = len(single_id_order_lines_df["order_id"].tolist())
        for i in range(order_length):
            # Get the product ID and amount in line of order lines in orders made on date
            product_id = single_id_order_lines_df.iloc[i]["product_id"]
            row_amount = single_id_order_lines_df.iloc[i]["total_amount"]

            # Check if product was being promoted on date
            if product_id in product_promotion_on_date:
                # Get promotion id and commission that order line generated
                promotion_id = date_product_promotions_df[date_product_promotions_df["product_id"] == product_id].iloc[0]["promotion_id"]
                promotion_commission = (row_amount * commission_rate)
                # pass as key, value pairs into promotions dictionary
                promotions[promotion_id].append(promotion_commission)

    # Create dict for commissions paid out per promotion with description as key, excluding promotions that did not generate orders on date
    promotion_descriptions = promotions_df["description"].tolist()
    commissions_per_promotion = {}
    for key, value in promotions.items():
        if len(value) != 0:
            total = sum(value)
            new_key = promotion_descriptions[key-1]
            commissions_per_promotion[new_key] = total

    total_commissions = sum(commissions)
    average_commission = average(commissions)

    ############################################################################
    # Results
    ############################################################################

    results = {
    "Total number of customers that made an order that day": customers_on_date,
    "Total number of items sold on that day": date_quantity,
    "The total amount of discount given that day": discount_on_date,
    "The average discount rate applied to the items sold that day": average_discount_on_date,
    "The average order total for that day": average_order_amount_on_date,
    "The total amount of commissions generated that day": total_commissions,
    "The average amount of commissions per order for that day": average_commission,
    "The total amount of commissions earned per promotion that day": commissions_per_promotion
    }

    with open('results_{}.csv'.format(date), 'w') as f:
        for key in results.keys():
            f.write("%s,%s\n"%(key,results[key]))

    try:
        return send_file('results_{}.csv'.format(date), as_attachment=True)
    except FileNotFoundError:
        abort(404)

    # return jsonify(results)
if __name__ == '__main__':
    app.run()



    #
