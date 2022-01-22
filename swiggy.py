import sys
import json
from datetime import datetime
import calendar

ORDER_IDS = set()


def get_food_items(order_items):
    food_items = ''
    for order_item in order_items:
        food_items += str(order_item['quantity']) + 'x' + order_item['name'] + ' '
    return food_items


def get_meal(date: str):
    order_time = date.split(' ')[1]
    hour = int(order_time.split(':')[0])
    if hour > 19:
        return "Dinner"
    if hour > 14:
        return "Lunch"
    if hour > 6:
        return "Breakfast"
    return "Dinner"


def get_day(date: str):
    date_time_obj = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
    return date_time_obj.strftime("%A")


def get_month(date: str):
    month_int = int(date.split('-')[1])
    return calendar.month_name[month_int]


def get_meal_type(order_items):
    for order_item in order_items:
        if order_item['is_veg'] == '0':
            return "Non-Veg"
    return "Veg"


def extract_orders(food_orders_resp):
    successful_orders = []
    for resp in food_orders_resp:
        orders_data = resp['data']['orders']
        for order_data in orders_data:
            order_id = str(order_data['order_id'])
            try:
                if order_id in ORDER_IDS:
                    continue
                ORDER_IDS.add(order_id)
                order_status = order_data['order_status']
                if order_status != 'Delivered':
                    continue
                food_items = get_food_items(order_data['order_items'])
                date = order_data['order_time'].strip()
                meal = get_meal(date)
                meal_type = get_meal_type(order_data['order_items'])
                day = get_day(date)
                month = get_month(date)
                year = date.split('-')[0]
                restaurant = order_data['restaurant_name']
                cost = str(order_data['net_total'])
                print('successful_order: ' + order_id)
                successful_orders.append(
                    [order_id, food_items, date, day, month, year, cost, restaurant, meal, meal_type])
            except Exception as e:
                print(order_id)
                print('exception is: ' + str(e))

    return successful_orders


def main(orders_path: str, csv_path: str):
    orders_file = open(orders_path)
    csv_file = open(csv_path, "w+")
    csv_file.write(
        "Order ID" + "\t" + "Food Items" + "\t" + "Date" + "\t" + "Day" + "\t" + "Month" + "\t" + "Year" + "\t" +
        "Cost" + "\t" + "Restaurant" + "\t" + "Meal" + "\t" + "Meal Type" + "\n")
    orders_data = json.load(orders_file)
    orders = extract_orders(orders_data['food_orders'])
    for order in orders:
        csv_file.write('\t'.join(order) + '\n')

    orders_file.close()
    csv_file.close()


if __name__ == "__main__":
    orders_path = sys.argv[1]
    csv_path = sys.argv[2]
    main(orders_path, csv_path)
