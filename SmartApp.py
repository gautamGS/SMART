import random
import SmartAppUtility
import SmartAppLibrary
import SmartMBA

from SmartAppUtility import *
from SmartAppLibrary import *
from SmartMBA import *

from flask import Flask
from flask import request
from random import randint


app = Flask(__name__)

PRD_IN_CONSIDERATION = 'brand1_prd1'
items = [
    {
        'id': 1,
        'address_1': u'images/1.jpg',
		'address_2': u'images/2.jpg',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol', 
        'done': False,
        'pie_chart_1' :[['Item','Competitor'], ['Apple',2], ['Orange',4],['Banana',1]],
        'pie_chart_2' :[['Brand','Competitor'], ['Samsung',3], ['Xiaomi',4]],
        'pie_chart_3' :[['Brand','Coverage'], ['Dell',3], ['HP',7]],
        'bounding_box_img' : u'images/3.jpg',
        'current_product_affinity' : 90
    },
    {
        'id': 2,
        'address_1': u'images/2.jpg',
		'address_2': u'images/1.jpg',
        'description': u'Cold Storage', 
        'done': False
    }
]


#  Entry level method for SMART analyzer.
#  It accpets aisle image path and product image path
#  as input and calls model pipeline to process
@app.route('/smart/analyze')
def analyze_aisle_image():
   ais_img=request.args.get('AIS_IMG', default='./ais_repo/ais1.png', type=str)
   prd_img=request.args.get('PRD_IMG', default='./prd_repo/prd1.png', type=str)
   req_no=randint(1, 1001)
   
   process_pipeline(ais_img, prd_img, req_no)
   return  ais_img + ' '+ prd_img + ' '+ str(req_no)
 
@app.route('/stg/items', methods=['GET']) 
def get_items():
    return jsonify({'items': items})

@app.route('/stg/items/<int:id>/<int:img_id>', methods=['GET'])
def selected_item(id, img_id):
	local_item = [item for item in items if item['id'] == id]
	if len(local_item) == 0:
		abort(404)
	return jsonify({'item': local_item[0]}) 
 
#
#
#
def process_pipeline(ais_img, prd_img, req_no):
    
    #Extract product bounding boxes
    dict_prd_bb = extract_prd_bb_coord(ais_img)
    print('dict_prd_bb ')
    print_dict(dict_prd_bb)
    
    #Extract promo bounding boxes
    dict_promo_bb = extract_promo_bb_coord(ais_img)
    print('dict_promo_bb ')
    print_dict(dict_promo_bb)
    
    #Classify each product item
    prd_dict = classify_prd_items(dict_prd_bb)
    print_dict(prd_dict)
    
    #Compute each item type
    count_dict = compute_dict_count(prd_dict)
    print_dict(count_dict)
    
    #Compute Overall Coverage
    prd_cvg_dict = compute_coverage_all(count_dict)
    print_dict(prd_cvg_dict)
    
    #Get current affinity
    avail_prds = prd_cvg_dict.keys()
    affin_dict = get_prd_affin(PRD_IN_CONSIDERATION, avail_prds)
    print_dict(affin_dict)
    
    #Get Recommendations
    max_affin_prd = get_max_affin(PRD_IN_CONSIDERATION)
    print(max_affin_prd)
    


#
#
#
def classify_prd_items(dict_prd_bb):
  prd_dict = {}
  for key,val in dict_prd_bb.items():
    for item in val:
      prd_label = product_matcher(key, item)
      if prd_label not in prd_dict:
        templist = [item]
        prd_dict[prd_label] = templist       
      else:
        temp_list = prd_dict[prd_label].append(item)
        prd_dict[prd_label] = prd_dict[prd_label]
  return prd_dict
    

  
#  Utility Functions



if __name__ == '__main__':
   app.run()