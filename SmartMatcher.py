import cv2
import matplotlib.pyplot as plt
import sys
import os.path
import numpy as np

def img_resize(file_nm, plt_ind = False):
    img2 = cv2.imread(file_nm)
    img2 = cv2.cvtColor(img2, cv2.COLOR_RGB2GRAY)
    #print("Before resize: ", img2.shape)
    if plt_ind:
        plt.subplot(1,2,1)
        plt.imshow(img2, cmap = 'gray')
        plt.subplot(1,2, 2)
        img2 = cv2.resize(img2, (283,490), interpolation =  cv2.INTER_CUBIC)
        plt.imshow(img2, cmap = 'gray')
    else:
        img2 = cv2.resize(img2, (283,490), interpolation =  cv2.INTER_CUBIC)
    #print("After resize: ", img2.shape)
    return img2

def drawMatches(img1, kp1, img2, kp2, matches):

    rows1 = img1.shape[0]
    cols1 = img1.shape[1]
    rows2 = img2.shape[0]
    cols2 = img2.shape[1]

    out = np.zeros((max([rows1,rows2]),cols1+cols2,3), dtype='uint8')
    out[:rows1,:cols1] = np.dstack([img1])
    out[:rows2,cols1:] = np.dstack([img2])
    for mat in matches:
        img1_idx = mat.queryIdx
        img2_idx = mat.trainIdx
        (x1,y1) = kp1[img1_idx].pt
        (x2,y2) = kp2[img2_idx].pt

        cv2.circle(out, (int(x1),int(y1)), 4, (255, 0, 0, 1), 1)   
        cv2.circle(out, (int(x2)+cols1,int(y2)), 4, (255, 0, 0, 1), 1)
        cv2.line(out, (int(x1),int(y1)), (int(x2)+cols1,int(y2)), (255, 0, 0, 1), 1)

    return out

def sift_compare(img1, img2):
    #img1 = cv2.imread(filename1)          # queryImage
    #img2 = cv2.imread(filename2)          # trainImage
    #if 
    # Initiate SIFT detector
    sift = cv2.xfeatures2d.SIFT_create()

    # find the keypoints and descriptors with SIFT
    kp1, des1 = sift.detectAndCompute(img1,None)
    kp2, des2 = sift.detectAndCompute(img2,None)

    # BFMatcher with default params
    #bf = cv2.BFMatcher()
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    matches = bf.knnMatch(des1,des2, k=2)
    #matches = bf.match(des1,des2)
    #matches = sorted(matches, key=lambda val: val.distance)

    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append(m)

    img3 = drawMatches(img1,kp1,img2,kp2,good[:25])
    # Show the image
    #cv2.imshow('Matched Features', img3)
    #cv2.waitKey(0)
    #cv2.destroyWindow('Matched Features')
    return len(good), img3
#if len(sys.argv) != 3:
#    sys.stderr.write("usage: compare.py <queryImageFile> <sourceImageFile>\n")
#    sys.exit(-1)

def orb_compare(img1, img2):
    #img1 = cv2.imread(filename1)          # queryImage
    #img2 = cv2.imread(filename2)          # trainImage

    # Initiate SIFT detector
    orb = cv2.ORB_create()
    
    # find the keypoints and descriptors with SIFT
    kp1, des1 = orb.detectAndCompute(img,None)
    kp2, des2 = orb.detectAndCompute(img2,None)

    # BFMatcher with default params
    #bf = cv2.BFMatcher()
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    matches = bf.knnMatch(des1,des2, k=2)
    #matches = bf.match(des1,des2)
    #matches = sorted(matches, key=lambda val: val.distance)

    # Apply ratio test
    good = []
    for m,n in matches:
        if m.distance < 0.75*n.distance:
            good.append(m)

    img3 = drawMatches(img1,kp1,img2,kp2,good[:25])
    # Show the image
    #cv2.imshow('Matched Features', img3)
    #cv2.waitKey(0)
    #cv2.destroyWindow('Matched Features')
    return len(good), img3

def match_product(search_img, ):
    prd_mstr_lst = ['ShreddedWheat.jpg', 'ABCAlphabits.jpg', 'cornflakes.jpg', 'RaisinBran.jpg']
    best_match_cnt = 0
    best_match_img = ''
    threshold = 50
    search_img = cv2.resize(cv2.cvtColor(search_img, cv2.COLOR_RGB2GRAY), \
                            (283,490), interpolation =  cv2.INTER_CUBIC)
    for ref_img_nm in prd_mstr_lst:
        ref_img = img_resize(ref_img_nm)
        good_match_cnt, matched_img = sift_compare(ref_img, search_img)
        if good_match_cnt > best_match_cnt:
            best_match_cnt = good_match_cnt
            best_img = matched_img
            best_match_img = ref_img_nm
        print("Significance value between ", ref_img_nm, " and search image is ", good_match_cnt )
    if best_match_cnt > threshold:
        return best_match_img
    else:
        return None
