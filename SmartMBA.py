#  SAMPLE_LIST = ['brand1_prd1', 'brand1_prd2', 'brand2_prd1', 'brand3_prd1', 'brand1_prd3', 'brand2_prd2']
AFFINITY_DICT = { 
  'brand1_prd1' : [('brand1_prd2', 80), ('brand2_prd1', 60), ('brand3_prd1', 10), ('brand1_prd3', 90), ('brand2_prd2', 80)],
  'brand1_prd2' : [('brand1_prd1', 70), ('brand2_prd1', 10), ('brand3_prd1', 20), ('brand1_prd3', 80), ('brand2_prd2', 70)],
  'brand2_prd1' : [('brand1_prd1', 60), ('brand1_prd2', 40), ('brand3_prd1', 40), ('brand1_prd3', 70), ('brand2_prd2', 60)],
  'brand3_prd1' : [('brand1_prd1', 50), ('brand1_prd2', 30), ('brand2_prd1', 40), ('brand1_prd3', 10), ('brand2_prd2', 50)]
}

COMPITITION_DICT = {
  'brand1': 'brand3'
}


def get_affinity(prd1, prd2):
  affin = 0
  affinities = AFFINITY_DICT[prd1]
  for item in affinities:
    print('Comparing ', item[0], ' and ', prd2)
    if item[0] == prd2:
      affin = item[1]
  return affin
  
def get_max_affin(prd):
  result = ()
  affin = 0
  affinities = AFFINITY_DICT[prd]
  for item in affinities:
    if item[1] > affin:
      result = item
      affin = item[1]
  return result
  
def get_prd_affin(prd, avail_prds):
  affin_dict = {}
  for prd2 in avail_prds:
    if prd != prd2:
      affin_dict[prd2] = get_affinity(prd, prd2)
  return affin_dict