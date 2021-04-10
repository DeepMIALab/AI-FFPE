import os
import sys
import cv2
import numpy
import fnmatch
import statistics
import argparse


argPar = argparse.ArgumentParser(description='frozen_ffpe')

argPar.add_argument("--input_path",required=True,help="input data path")
argPar.add_argument("--delete",required=True,help="delete eliminated files immediately or move to output directory")
argPar.add_argument("--output_path",required=False,help="output data path")
args = argPar.parse_args()

def find_avg_color(index,avg_r="",avg_g="",avg_b="",r_mean="",g_mean="",b_mean="",bool=False):
    image = cv2.imread(list_im[index])
    avg_color_per_row = numpy.average(image, axis=0)
    avg_color = numpy.average(avg_color_per_row, axis=0)
    if bool == True:
        avg_r.append(avg_color[2])
        avg_g.append(avg_color[1])
        avg_b.append(avg_color[0])
    return avg_color

path= args.input_path
delete_or_remove=args.delete
if args.output_path is not None:
    trash_path= args.output_path
    if not os.path.exists(trash_path):
        os.mkdir(trash_path)


image_names=[f for f in sorted(os.listdir(path)) if fnmatch.fnmatch(f, '*.png')]
list_im=[path+"/"+ f for f in image_names]
discarded_images=[]
number_of_images=len(list_im)
print("Number of images: ", number_of_images)
avg_r=[]
avg_g=[]
avg_b=[]

r_mean=0.0
g_mean=0.0
b_mean=0.0

for index in range(0,number_of_images):
    avg_color=find_avg_color(index,avg_r,avg_g,avg_b,r_mean,g_mean,b_mean,True)
    r_mean+=avg_color[2]
    g_mean+=avg_color[1]
    b_mean+=avg_color[0]
    
    
for index in range(0,number_of_images):
    file=list_im[index]
    name=image_names[index]
        
    avg_color=find_avg_color(index,False)


    if not (150<avg_color[2]<217 and 80<avg_color[1]<185 and 130 <avg_color[0] < 205) :
        discarded_images.append(list_im[index])
        
        if delete_or_remove=="True":
            os.remove(file)
        else:
            os.rename(file, trash_path+"/"+'{}'.format(name))
print("Number of discarded images from the data set {} is: {} \n".format(path,len(set(discarded_images))))
  