import time
import redis
from main import r, Order

key = "refund_order"

group = "payment-group"

try:
    r.xgroup_create(key, group, id="0", mkstream=True)
except redis.exceptions.ResponseError as error:
    if "BUSYGROUP" not in str(error):
        raise

while True:
    try:
        results = r.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            print(results)
            for result in results:
                obj = result[1][0][1]
                order = Order.get(obj['pk'])
                order.status = "refunded"
                order.save()
               
    except Exception as e:
        print(str(e))
    time.sleep(1)
