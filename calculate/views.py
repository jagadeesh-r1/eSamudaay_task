from django.http import HttpResponse
from rest_framework.response import Response
from typing import Dict
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
import bisect

distance_ranges = [0,10000     ,10001,20000      ,20001,50000      ,50001,500000] #in Kilometers
delivery_charges = { 
    0: 5000,
    2: 10000,
    4: 50000,
    6: 100000
} # in Paisa


@csrf_exempt
def index(request):
    return HttpResponse("Hello! eSamudhaay")


@csrf_exempt
@api_view(['POST'])
def calculate(request):
    """
    This function is used to check for mandatory fields and call the calculate_value function
    """
    request_data = request.data
    mandatory_fields = ["order_items","distance"]
    missing_fields = []
    for field in mandatory_fields:
        if field not in request_data:
            missing_fields.append(field)
    if missing_fields:
        response = {
            "status" : False,
            "message" :{
                "ERRORMSG" : "MANDATORY_FIELDS_MISSING",
                "message" : "The field(s) {} is/are missing in the request body".format(",".join(missing_fields)) 
            }
        }
        return Response(response)
    order_value = calculate_value(request_data)

    return Response(order_value)

def calculate_value(request_data: Dict):
    """
    Calculate order value on the basis of order items and their given prices. We have to calculate the delivery charge based on distance
    Have to deduct offer value if its valid
    """
    order_value = 0
    order_offer = None
    order_items = request_data.get("order_items")
    order_distance = request_data.get("distance")
    if order_distance > distance_ranges[-1]:
        response = {
                "status" : False,
                "message" :{
                    "ERRORMSG" : "INVALID_DISTANCE_VALUE",
                    "message" : "Distance given is not valid" 
                }
            }
        return response
    if request_data.get("offer"):
        order_offer = request_data.get("offer")

    for item in order_items:
        order_value += item["quantity"] * item["price"]
    '''
    Bisect is used here to search the range index where the distance is going to be. It is used instead of if/else statements as bisect uses binary search which is faster
    than conditional statements.
    '''
    index = bisect.bisect_left(distance_ranges,(order_distance))
    delivery_charge = delivery_charges[index if index%2 == 0 else index-1]
    print(index,delivery_charge)
    total_order_value = order_value + delivery_charge
    print("total",total_order_value)
    if order_offer:
        if order_offer["offer_type"] == "FLAT":
            if order_offer["offer_val"] < total_order_value:
                total_order_value -= order_offer["offer_val"]
            else:
                response = {
                    "status" : False,
                    "message" :{
                        "ERRORMSG" : "INVALID_OFFER_VALUE",
                        "message" : "Offer value greater than order value" 
                    }
                }
                return response
        elif order_offer["offer_type"] == "DELIVERY":
            total_order_value -= delivery_charge
        else:
            response = {
                "status" : False,
                "message" :{
                    "ERRORMSG" : "INVALID_OFFER_CODE",
                    "message" : "Offer code is not valid" 
                }
            }
            return response
    response = {
        "order_total" : total_order_value
    } 
    return response