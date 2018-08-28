import random
import SmartMatcher

from SmartMatcher import *
from random import randint


# Extract and label bounding boxes for individual
# product item and product group.
# REPLACE THIS FUNCTION WITH THE MODEL LIBRARY
def extract_prd_bb_coord(ais_img):
    PRD_DICT = { 
               'C1' : [[[10,20],[30,40]], [[60,70],[90,100]]],
               'C2' : [[[35,65],[80,94]], [[12,20],[80,60]]] 
             }
    return PRD_DICT
    

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
def product_matcher(category, img_bb_coord):
  SAMPLE_LIST = ['brand1_prd1', 'brand1_prd2', 'brand2_prd1', 'brand3_prd1']
  return random.choice(SAMPLE_LIST)
  