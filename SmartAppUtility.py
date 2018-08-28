#
#
#
def compute_dict_count(dict):
  result_dict = {}
  for key,val in dict.items():
    result_dict[key] = len(val)
  return result_dict
  
#
#
#
def compute_coverage_all(dict):
  result_dict = {}
  total_items = 0
  for key,val in dict.items():
    total_items = total_items + val
  for key,val in dict.items():
    result_dict[key] = val / total_items * 100
  return result_dict
   
#
#
#
def print_dict(dict):
  for key,val in dict.items():
    print(key, "=>", val)