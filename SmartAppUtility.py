import cv2
from datetime import datetime

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
    result_dict[key] = round(val / total_items * 100, 2)
  return result_dict
   

#
#
def print_dict(dict, dict_name = 'DICT_NAME_UNKNOWN'):
  print(dict_name)
  for key,val in dict.items():
    print(key, "=>", val)


#
def load_image(image_path):
  return cv2.imread(image_path)

def get_current_timestamp():
  return datetime.now().microsecond 