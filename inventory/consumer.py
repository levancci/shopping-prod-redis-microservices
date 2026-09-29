import time

from main import r, Product

key = "order_completed"

group = "inventory-group"

try:
    r.xgroup_create(key, group)
except:
    print("Group already exists!")

while True:
    try:
        results = r.xreadgroup(group, key, {key: '>'}, None)

        if results != []:
            for result in results:
                obj = result[1][0][1]

                try:    
                    product = Product.get(obj['product_id'])
                    print(product)
                    product.quantity -= int(obj['quantity'])
                    product.save()  

                except Exception as e:
                    print(str(e))
                    r.xadd('refund_order', obj, '*')  
                    
    except Exception as e:
        print(str(e))
    time.sleep(1)
