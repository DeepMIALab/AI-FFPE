import matplotlib.pyplot as plt
import h5py
import glob
from natsort import natsorted
import os 
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--input-path',type=str,help='input for .h5')
parser.add_argument('--output-path',type=str,help='output for png')
args = parser.parse_args()
image_list = []
im_cntr1 = 0

im_cntr2_list = []

input_path = args.input_path
output_path = args.output_path

#input_path = "./path2svs/"
#output_path = "/path2png/"
output_path = os.path.join(output_path,"png_patches/testA/")
print(output_path)
os.makedirs(output_path)
h5_counter = 0
exception_list = []

for filem in natsorted(glob.glob(input_path+"*.h5")):
    print("h5 count",h5_counter)
    h5_counter+=1
    print(filem) 
    try: 
        png_cntr = 0        
        hdf = h5py.File(filem)             
        for i in list(hdf['imgs']):
            plt.imsave(output_path+filem.split("/")[-1]+"_"+str(png_cntr) +".png",i)
            png_cntr+=1
            print(png_cntr)
    except:
        exception_list.append(filem.split("/")[-1])
        print("Exception occured!!!")
        pass



#im_counter = 0 
#for image in sorted(glob.glob(filename_list+"/*")):
    #print(image.split("/")[-1])
    #if domain_type in image:
        #imagename = "/a"+str(im_counter)
        #shutil.copy(image,output_folder_name+"/"+image.split("/")[-1])
        #im_counter += 1
