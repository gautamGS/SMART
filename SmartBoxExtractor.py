import cv2
from SmartRect import Rectangle
from SmartAppUtility import *
from SmartAppConfig import *

gp_coords = [[[0,0],[584,274]],
							[[5,319],[581,696]],
							[[210,731],[581,1023]],
							[[67,787],[211,989]]]

prd_coords = [[[5,7],[97,273]],
							[[85,35],[273,267]],
							[[299,7],[475,253]],
							[[495,11],[583,255]],
							[[6,469],[81,641]],
							[[79,463],[237,683]],
							[[247,439],[377,695]],
							[[393,465],[575,677]],
							[[215,817],[325,961]],
							[[315,835],[433,1009]],
							[[443,819],[563,1007]],
							[[99,811],[191,977]]]

def get_img_with_bb(img_path, coords):
	img = cv2.imread(img_path)
	img_with_bb = img
	disp_img = cv2.resize(img_with_bb, (OP_DISP_WIDTH, OP_DISP_HEIGHT)) 
	for coord in coords:
		(x1, x2, y1, y2) = extract_xy(coord)
		print('(',x1,',',y1,')', ' (',x2,',',y2,')')
		img_with_bb = draw_rect(img_with_bb, x1, y1, x2, y2, (0, 255, 255))
	op_image_path = "{}/{}.png".format(OUTPUT_FOLDER, get_current_timestamp())
	print('op_image_path ', op_image_path)
	cv2.imwrite( op_image_path, img_with_bb)
	return op_image_path

#returns x1, x2, y1, y2
def extract_xy(coord):
	return (coord[0][0], coord[1][0], coord[0][1], coord[1][1])

def draw_rect(img, x1, y1, x2, y2, color):
	cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
	return img

def group_bb(gp_coords, prd_coords):
	bb_grp_dict={}
	for prd_coord in prd_coords:
		(x1, x2, y1, y2) = extract_xy(prd_coord)
		p_rect = Rectangle(x1, x2, y1, y2)
		gp_ndx = get_gp_bb(p_rect)
		if gp_ndx is not -1:
			if gp_ndx not in bb_grp_dict:
				templist = [prd_coord]
				bb_grp_dict[gp_ndx] = templist
			else:
				temp_list = bb_grp_dict[gp_ndx].append(prd_coord)
				bb_grp_dict[gp_ndx] = templist
	print_dict(bb_grp_dict)
	return bb_grp_dict

def get_gp_bb(rect):
	for index, gp_coord in enumerate(gp_coords):
		(x1, x2, y1, y2) = extract_xy(gp_coord)
		g_rect = Rectangle(x1, x2, y1, y2)
		containment_resutl = rect.is_contained_by(g_rect)
		if containment_resutl is not False:
			#print('Box ', rect, ' is contained by ', g_rect)
			return index
	return -1

#group_bb(gp_coords, prd_coords)

#img = cv2.imread('./ais_repo/ais1.png')
#img_with_bb = draw_bb(img, gp_coords)
#disp_img = cv2.resize(img_with_bb, (DISP_WIDTH, DISP_HEIGHT)) 
#cv2.imshow('image',disp_img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
