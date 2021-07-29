#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 27 22:02:14 2020

@author: bou02
"""

import math
import os
import time
import xml.etree.ElementTree as ET
from xml.dom import minidom
import sys
import fnmatch
from glob import glob
import cv2
import matplotlib.pyplot as plt
import numpy as np
import openslide
from PIL import Image
import PIL
PIL.Image.MAX_IMAGE_PIXELS = 9000000000
import pdb
import h5py
import math
from wsi_core.wsi_utils import savePatchIter_bag_hdf5, initialize_hdf5_bag
from numpy import ones
import re 
import argparse


parser = argparse.ArgumentParser(description='FrozGAN Stitching',formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--down-ratio', default=1, type=int, help='stitching downscale ratio')
parser.add_argument('--h5-inpath', type=str, help='.h5 path')

parser.add_argument('--preds-path', type=str, help='FrozGAN preds path')
parser.add_argument('--output-dir', type=str, help='output path')

args = parser.parse_args()

def load_image( infilename ) :
    img = Image.open( infilename )
    img.load()
    data = np.asarray( img, dtype="uint8" )
    return data

def DrawGrid(img, coord, shape, thickness=2, color=(0,0,0,255)):
    cv2.rectangle(img, tuple(np.maximum([0, 0], coord-thickness//2)), tuple(coord - thickness//2 + np.array(shape)), (0, 0, 0, 255), thickness=thickness)
    return img

def DrawMap(canvas, patch_dset, coords, patch_size, indices=None, verbose=1, draw_grid=True):
    if indices is None:
        indices = np.arange(len(coords))
    total = len(indices)
    if verbose > 0:
        ten_percent_chunk = math.ceil(total * 0.1)
       # print('start stitching {}'.format(patch_dset.attrs['wsi_name']))
    
    for idx in range(total):
        if verbose > 0:
            if idx % ten_percent_chunk == 0:
                print('progress: {}/{} stitched'.format(idx, total))
        
        patch_id = indices[idx]
        print(patch_id)
        patch = patch_dset[patch_id]
        patch = cv2.resize(patch, patch_size)
        coord = coords[patch_id]
        print(coord)
        canvas_crop_shape = canvas[coord[1]:coord[1]+patch_size[1], coord[0]:coord[0]+patch_size[0], :3].shape[:2]
        canvas[coord[1]:coord[1]+patch_size[1], coord[0]:coord[0]+patch_size[0], :3] = patch[:canvas_crop_shape[0], :canvas_crop_shape[1], :]
        if draw_grid:
            DrawGrid(canvas, coord, patch_size)

    return Image.fromarray(canvas)

def StitchPatches(hdf5_file_path, pred_path,downscale=4, draw_grid=False, bg_color=(0,0,0), alpha=-1):
    file = h5py.File(hdf5_file_path, 'r')
    files = []
    dset = file['imgs']
    print(len(dset))   
    start_dir = pred_path
    pattern = "*.png"
    for dir,_,_ in os.walk(start_dir):
        files.extend(glob(os.path.join(dir,pattern)))
    print(len(files))
    files.sort(key=lambda f: int(re.sub('\D', '', f)))
    
    images = ones((len(files), 512, 512, 3))
    for i,load in enumerate(files):
        print(load)
        images[i]=(load_image( load ))
    print(images[0].dtype)
    #dset=files
    coords = file['coords'][:]
    if 'downsampled_level_dim' in dset.attrs.keys():
        w, h = dset.attrs['downsampled_level_dim']
    else:
        w, h = dset.attrs['level_dim']
    print('original size: {} x {}'.format(w, h))
    w = w // downscale
    h = h //downscale
    coords = (coords / downscale).astype(np.int32)
    print('downscaled size for stiching: {} x {}'.format(w, h))
    print('number of patches: {}'.format(len(dset)))
    img_shape = dset[0].shape
    print('patch shape: {}'.format(img_shape))
    downscaled_shape = (img_shape[1] // downscale, img_shape[0] // downscale)
    
    if w*h > Image.MAX_IMAGE_PIXELS: 
        raise Image.DecompressionBombError("Visualization Downscale %d is too large" % downscale)
    
    if alpha < 0 or alpha == -1:
        heatmap = Image.new(size=(w,h), mode="RGB", color=bg_color)
    else:
        heatmap = Image.new(size=(w,h), mode="RGBA", color=bg_color + (int(255 * alpha),))
    
    heatmap = np.array(heatmap)
    heatmap = DrawMap(heatmap, images, coords, downscaled_shape, indices=None, draw_grid=draw_grid)
       
    file.close()
    return heatmap
down_ratio = args.down_ratio
for i in glob(str(args.h5_inpath)+"/*.h5"):
	h5_path = i

preds_path = args.preds_path
heatmap=StitchPatches(h5_path,preds_path, down_ratio)
out_path = args.output_dir
stitch_path = os.path.join(out_path, "fake_stitch"+'.png')
heatmap.save(stitch_path)
