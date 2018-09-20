from helper import jsonify_offer_list,get_offers,get_huge_savings
from flask import Flask,request
app = Flask(__name__)

@app.route('/gethugesavings',methods=['GET'])
def get_huge_savings_items():
    save_items_name,save_items_price,save_items_save_value = get_huge_savings()
    response_data = jsonify_offer_list(save_items_name,save_items_price,save_items_save_value)
    return response_data


@app.route('/getoffers',methods=['GET'])
def get_offers_items():
    threshold_price = request.args.get('thresholdprice')
    if threshold_price != None:
        threshold_price = float(threshold_price)
    items_name,items_prices,items_save_value,_ = get_offers(threshold_price)
    response_data = jsonify_offer_list(items_name,items_prices,items_save_value)
    return response_data
