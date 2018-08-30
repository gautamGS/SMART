import random
import json

from SmartBoxExtractor import *
from SmartAppUtility import *
from SmartAppLibrary import *
from SmartMBA import *
from SmartAppConfig import *

from flask import Flask, jsonify, make_response
from flask import request
from random import randint


app = Flask(__name__)

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
   
   return process_pipeline(ais_img, prd_img, req_no) 
 #
 #
 #
 #
@app.route('/smart/products')
def get_products():
  prds_with_brand = get_all_prds_and_brands()
  resp = json.dumps(prds_with_brand)
  resp.headers['Access-Control-Allow-Origin'] = '*'
  return resp

@app.route('/stg/items', methods=['GET']) 
def get_items():
    resp = jsonify({'items': items})
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route('/stg/items/<int:id>/<int:img_id>', methods=['GET'])
def selected_item(id, img_id):
  local_item = [item for item in items if item['id'] == id]
  if len(local_item) == 0:
    abort(404)
  else:
    json_res = jsonify({'item': local_item[0]})
    resp = make_response(json_res)
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp
 
#
#
#
def process_pipeline(ais_img_path, prd_img_path, req_no):
    
  #
  #Fetch Images
  ais_img = load_image(ais_img_path)
  prd_img = load_image(prd_img_path)

  #Extract product bounding boxes
  prd_bb_coords = extract_prd_bb_coord(ais_img)
  print('Total product items ', len(prd_bb_coords))

  op_image = get_img_with_bb(ais_img_path, prd_bb_coords)

  gp_bb_coords = extract_grp_bb_coord(ais_img)   
  
  #Extract promo bounding boxes
  promo_bb_coords = extract_promo_bb_coord(ais_img)

  #Group items
  group_bb(gp_bb_coords, prd_bb_coords)
  
  #Classify each product item
  prd_dict = classify_prd_items(prd_bb_coords)
  print_dict(prd_dict,'Classified Products')
  
  #Compute each item type
  count_dict = compute_dict_count(prd_dict)
  print_dict(count_dict, 'Product Count')

  #Compute competitive coverage
  comp_cvg_dict = compute_coverage_all(
    compute_comp_dict(count_dict, PRD_IN_CONSIDERATION, COMPETITORS))
  print_dict(comp_cvg_dict, "Competition Cvg")

  brand_cvg_dict = compute_brand_coverage(count_dict, PRD_IN_CONSIDERATION)
  print(brand_cvg_dict)

  #Compute Overall Coverage
  prd_cvg_dict = compute_coverage_all(count_dict)
  print_dict(prd_cvg_dict, 'Product Covreage %')    
  
  #Get current affinity
  avail_prds = prd_cvg_dict.keys()
  affin_dict = get_prd_affin(PRD_IN_CONSIDERATION, avail_prds)
  print_dict(affin_dict, "affinity_dict")
  
  #Get Recommendations
  max_affin_prd = get_max_affin(PRD_IN_CONSIDERATION)
  print_dict(max_affin_prd)

  print('Creating op dict')
  #Create an op dict
  op_dict = {}
  op_dict['prd_cvg_pc'] = format_dict_for_json(prd_cvg_dict)
  op_dict['cmp_cvg_pc'] = format_dict_for_json(comp_cvg_dict)
  op_dict['brn_cvg_pc'] = brand_cvg_dict
  op_dict['afn_cvg_bg'] = format_dict_for_json(affin_dict)
  op_dict['max_aff_bg'] = format_dict_for_json(max_affin_prd)
  op_dict['out_img_bb'] = op_image

  #convert op dict to json
  print('Creating op json')
  op_json = json.dumps(op_dict)  
  return op_json
#
#
def classify_prd_items(dict_prd_bb):
  prd_dict = {}
  for item in dict_prd_bb:
    prd_label = product_matcher(item)
    if prd_label not in prd_dict:
      templist = [item]
      prd_dict[prd_label] = templist       
    else:
      temp_list = prd_dict[prd_label].append(item)
      prd_dict[prd_label] = prd_dict[prd_label]
  return prd_dict
    

def format_dict_for_json(dict):
  op_dict = {}
  for key, val in dict.items():
    mapped_key=get_brand_and_prd(key)
    op_dict['{}_{}'.format(mapped_key[0], mapped_key[1])]= val
  return  op_dict
#  Utility Functions

#process_pipeline('./ais1.png', './ais1.png', 1001)

if __name__ == '__main__':
  app.run(host='0.0.0.0')