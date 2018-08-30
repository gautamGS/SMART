import random

from SmartMatcher import *
from SmartMBA import *
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
def product_matcher(img_bb_coord):
  OP_KEY_VAL = 1
  total_prds = get_prd_list()
  filtered_prds = total_prds
  if PRD_ID_NOT_TO_MATCH is not 0:
    for prd in filtered_prds:
      if prd[1] == PRD_ID_NOT_TO_MATCH:
        filtered_prds.remove(prd)
        break
  picked_prd = random.choice(filtered_prds)
  brand_prd = (get_brand_from_prdID(picked_prd[OP_KEY_VAL]), picked_prd[OP_KEY_VAL])
  return brand_prd
  