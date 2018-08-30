from collections import OrderedDict
from SmartAppConfig import *


def get_affinity(prd1, prd2):
  affin = 0
  affinities = AFFINITY_DICT[prd1]
  for item in affinities:
    if item[0] == prd2:
      affin = item[1]
  return affin
  
def get_max_affin(prd):
  result = ()
  affin = 0
  affinities = AFFINITY_DICT[prd]
  for item in affinities:
    if item[1] > affin:
      affin = item[1]
      result = item
  return {(get_brand_from_prdID(result[0]), result[0]) : result[1]}
  
def get_prd_affin(prd, avail_prds):
  affin_dict = {}
  for prd2 in avail_prds:
    prdID = prd2[1]
    if prd != prdID:
      affin_dict[prd2] = get_affinity(prd, prdID)
      #affin_dict[get_brand_and_prd(prd2)] = get_affinity(prd, prdID)
  return OrderedDict(sorted(affin_dict.items(), key=lambda x:x[1], reverse=True))

def get_brand_and_prd(brand_prd_tuple):
  return((BRAND_DICT.get(brand_prd_tuple[0]), get_prd_name_from_id(brand_prd_tuple[1])))

def get_brand_from_prdID(prdID):
  for key, val in PRODUCT_DICT.items():
    for prd in val:
      if prd[1] == prdID:
        return key

def get_prd_name_from_id(prdID):
  for prd in get_prd_list():
    if prd[1] == prdID:
      return prd[0]

def get_prd_list():
  prds = PRODUCT_DICT.values()
  total_prds = [item for sublist in prds for item in sublist]
  return total_prds

def get_all_prds_and_brands():
  pb_dict = {}
  for key, val in PRODUCT_DICT.items():
    brandName = BRAND_DICT.get(key)
    for prd in val:
      prdName = prd[0]
      if brandName not in pb_dict:
        templist = [prdName]
        pb_dict[brandName] = templist
      else:
        pb_dict[brandName].append(prdName)
        #pb_dict[brandName] = templist
  return pb_dict

def compute_comp_dict(dict, prdID, COMPETITORS):
  comp_brands = []
  prd_brand = get_brand_from_prdID(prdID)
  for competitor_gp in COMPETITORS:
    for brand in competitor_gp:
      if brand == prd_brand:
        comp_brands = competitor_gp
        break
  comp_dict = {}
  for key, val in dict.items():
    if key[0] in comp_brands:
      comp_dict[key] = val
  return comp_dict

def compute_brand_coverage(dict, prdID):
  brand_covg_dict = {}
  prd_brand = get_brand_from_prdID(prdID)
  total_prds_in_brand = len(PRODUCT_DICT[prd_brand])
  brand_covg_dict['total_products'] = total_prds_in_brand
  covered_prds = 0
  for key, val in dict.items():
    if key[0] == prd_brand:
      covered_prds = covered_prds + 1
  brand_covg_dict['current_products'] = covered_prds
  return brand_covg_dict
