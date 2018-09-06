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
@app.route('/smart/analyze', methods = ['POST'])
def analyze_aisle_image():
   print('request.args ', request.form)
   ais_img=request.form.get('AIS_IMG', default='./ais_repo/ais1.png', type=str)
   brand=request.form.get('BRAND', type=str)
   item=request.form.get('ITEM', type=str)
   req_no=randint(1, 1001) 
   ais_img = './ais_repo/ais1.png'
   response_text = process_pipeline(ais_img, brand, item)
   resp = make_response(json.dumps(response_text))
   resp.headers['Access-Control-Allow-Origin'] = '*'
   return resp


@app.route('/smart/test', methods = ['GET'])
def analyze_aisle_image_test():
   ais_img=request.args.get('AIS_IMG', default='./ais_repo/ais1.png', type=str)
   prd_img=request.args.get('PRD_IMG', default='./prd_repo/prd1.png', type=str)
   req_no=randint(1, 1001)
   response_text = process_pipeline(ais_img, prd_img, req_no)
   resp = make_response(json.dumps(response_text))
   resp.headers['Access-Control-Allow-Origin'] = '*'
   return resp
 #
 #
 #
 #
@app.route('/smart/products')
def get_products():
  prds_with_brand = get_all_prds_and_brands()
  resp = make_response(json.dumps(prds_with_brand))
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
def process_pipeline(ais_img_path, brand, item):
    
  #
  #Fetch Images
  ais_img = load_image(ais_img_path)

  print('brand', brand, ' ; item ', item)

  item_key = get_prdID_from_product(item)
  brand_key = get_brandID_from_brand(brand)

  print('brand', brand_key, ' ; item ', item_key)

  #Fetch Product
  PRD_IN_CONSIDERATION = (brand_key, item_key)
  print('PRD_IN_CONSIDERATION ', PRD_IN_CONSIDERATION)

  #Extract product bounding boxes
  prd_bb_coords = extract_prd_bb_coord(ais_img)
  print('Total product items ', len(prd_bb_coords))

  op_image = get_img_with_bb(ais_img_path, prd_bb_coords)

  #
  # Currently commenting this code. 
  # We can bring this back once YOLO for group detection
  # is ready.
  #gp_bb_coords = extract_grp_bb_coord(ais_img)   
  
  #Extract promo bounding boxes
  #promo_bb_coords = extract_promo_bb_coord(ais_img)

  #Group items
  #group_bb(gp_bb_coords, prd_bb_coords)
  
  #Classify each product item
  prd_dict = classify_prd_items(ais_img, prd_bb_coords)
  print_dict(prd_dict,'Classified Products')
  
  #Compute each item type
  count_dict = compute_dict_count(prd_dict)
  print_dict(count_dict, 'Product Count')

  #Compute competitive coverage
  comp_cvg_dict = compute_coverage_all(
    compute_comp_dict(count_dict, PRD_IN_CONSIDERATION, COMPETITORS))
  print_dict(comp_cvg_dict, "Competition Cvg")

  brand_cvg_dict = compute_brand_coverage(count_dict, PRD_IN_CONSIDERATION)
  print(brand_cvg_dict, 'Brand Coverage')

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
  op_dict['brn_cvg_pc'] = format_dict_for_json(brand_cvg_dict, False)
  op_dict['afn_cvg_bg'] = format_dict_for_json(affin_dict)
  op_dict['max_aff_bg'] = format_dict_for_json(max_affin_prd)
  op_dict['out_img_bb'] = op_image

  #convert op dict to json
  print('Creating op json')
  return op_dict
#
#
def classify_prd_items(ais_img, dict_prd_bb):
  prd_dict = {}
  matched_prd_dict = product_matcher(ais_img, dict_prd_bb)   
  return matched_prd_dict

def format_dict_for_json(dict, labelize=True):
  op_dict = []
  for key, val in dict.items():
    if (labelize):
      if (isinstance(key, tuple)):
        mapped_key=get_brand_and_prd(key)
        op_dict.append(['{}_{}'.format(mapped_key[0], mapped_key[1]), val])
      else:
        mapped_key = get_brand_from_brandID(key)
        op_dict.append([mapped_key, val])
    else:
      op_dict.append([key, val])
      
    #/op_dict['{}_{}'.format(mapped_key[0], mapped_key[1])]= val
    
    
  return  op_dict
#  Utility Functions

#process_pipeline('./ais1.png', './ais1.png', 1001)

if __name__ == '__main__':
  app.run(host='0.0.0.0')