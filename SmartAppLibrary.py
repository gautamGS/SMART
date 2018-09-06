import random

from SmartMatcher import *
from SmartMBA import *
from SmartBoxExtractor import *
from random import randint


# Extract and label bounding boxes for individual
# product item and product group.
# REPLACE THIS FUNCTION WITH THE MODEL LIBRARY
def extract_prd_bb_coord(ais_img):
    PRD_DICT = { 
               'C1' :[[[5,7],[97,273]],[[85,35],[273,267]],[[299,7],[475,253]],
               [[495,11],[583,255]],[[6,469],[81,641]],[[79,463],[237,683]]],
               'C2' : [[[247,439],[377,695]],[[393,465],[575,677]],[[215,817],[325,961]],
              [[315,835],[433,1009]],[[443,819],[563,1007]],[[99,811],[191,977]]] 
             }
    val = PRD_DICT.values()
    return  [item for sublist in val for item in sublist]    

# Extract and label bounding boxes for product group
# group item and product group.
# REPLACE THIS FUNCTION WITH THE MODEL LIBRARY
def extract_grp_bb_coord(ais_img):
    GRP_DICT = { 
               'C1' : [[[0,0],[584,274]],[[5,319],[581,696]],[[210,731],[581,1023]]],
               'C2' : [[[67,787],[211,989]]]
             }
    val = GRP_DICT.values()
    return  [item for sublist in val for item in sublist]


# Extract bounding boxes for promotional content.
# REPLACE THIS FUNCTION WITH THE MODEL LIBRARY
def extract_promo_bb_coord(ais_img):
    PROMO_DICT= { 
               'P1' : [[[10,20],[30,40]], [[60,70],[90,100]]],
               'P2' : [[[35,65],[80,94]], [[12,20],[80,60]]] 
             }
    return PROMO_DICT
    
#
#
#
def product_matcher(ais_image, img_bb_coord):
  OP_KEY_VAL = 1
  prd_master_list = get_product_master_list()
  print('Product Master list')
  for pm in prd_master_list:
    print(pm)
  if (USE_MATCHER_STUB == True):
    picked_prd = random.choice(prd_master_list)
    brand_prd = (get_brand_from_prdID(picked_prd[OP_KEY_VAL]), picked_prd[OP_KEY_VAL])
    return brand_prd
  else:
    #Extract desired image
    prd_dict = {}
    for img_bb in img_bb_coord:
      extracted_img = extract_sub_image(ais_image, img_bb)
      print('Maching ', img_bb)
      match = match_product(extracted_img, prd_master_list)
      if (match is not None):
        prdID = int(match.split('.')[-2].split('/')[-1])
        print("Match response ", match, ' prdID ', prdID)
        brand_n_prd =  (get_brand_from_prdID(prdID), prdID)
        if brand_n_prd not in prd_dict:
          prd_dict[brand_n_prd] = img_bb
        else:
          temp_list = prd_dict[brand_n_prd].append(img_bb)
          prd_dict[brand_n_prd] = prd_dict[brand_n_prd]
      else:
        print("No match happened")
    return prd_dict

#def find_match_for_image(img_bb_coord, prd_master_list):
  


def get_product_master_list():
  total_prds = get_prd_list()
  filtered_prds = total_prds
  if PRD_ID_NOT_TO_MATCH is not 0:
    for prd in filtered_prds:
      if prd[1] == PRD_ID_NOT_TO_MATCH:
        filtered_prds.remove(prd)
        break
  print('Filtered product list', filtered_prds)
  prd_master_list = []
  for prd in filtered_prds:
    prd_master_list.append("{}/{}.jpg".format(PRD_MASTER_REPO, prd[1]))
  return prd_master_list
