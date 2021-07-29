from natsort import natsorted
import glob
import shutil
import matplotlib.pyplot as plt
import h5py
import argparse

parser = argparse.ArgumentParser(description='Script for preperaing dataset by considering patient ID',
                                 formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument("--frozen-dir", required=True, type=str, help="input frozen .h5 path")
parser.add_argument("--ffpe-dir", required=True, type=str, help="input FFPE .h5 path")
parser.add_argument("--train-thresh", default=0.7,type=int, help="ratio of the training set")
parser.add_argument("--test-thresh", default=0.1,type=int, help="ratio of the test set")
parser.add_argument("--output-dir", type=str, help="Directory to prepare the dataset")
args = parser.parse_args()





frozen_path = os.path.join(args.frozen_dir, "*.h5")
case_id_list = []

for image_path in natsorted(glob.glob(frozen_path)):   
    case_id = image_path.split("/")[-1]
    case_id_list.append(case_id.split("-")[0] +"-"+ case_id.split("-")[1]+"-"+ case_id.split("-")[2])

case_unique = set(case_id_list)

ffpe_path = os.path.join(args.ffpe_dir, "*.h5")
case_id_list2 = []

for image_path in natsorted(glob.glob(ffpe_path)):   
    case_id = image_path.split("/")[-1]
    case_id_list2.append(case_id.split("-")[0] +"-"+ case_id.split("-")[1]+"-"+ case_id.split("-")[2])

case_unique2 = set(case_id_list2)

case_intersect = case_unique.intersection(case_unique2)
set_divider = 0
train_id = []
val_id = []
test_id = []
for m, case_id in enumerate(case_intersect):
    if set_divider < int(len(case_intersect)*args.train_thresh):
        train_id.append(case_id)
    elif int(len(case_intersect)*args.train_thresh) < set_divider < int(len(case_intersect)*args.train_thresh+args.test_thresh):
        val_id.append(case_id)
    else :
        test_id.append(case_id)       
    set_divider+=1

train_output = os.path.join(args.output_dir,"trainB")
val_output = os.path.join(args.output_dir,"valB")
test_output = os.path.join(args.output_dir,"testB") 

for file in natsorted(glob.glob(ffpe_path)):   
    case_id = file.split("/")[-1]
    png_cntr = 0

    if (case_id.split("-")[0] +"-"+ case_id.split("-")[1]+"-"+ case_id.split("-")[2]) in train_id:
        hdf = h5py.File(file)
        for i in list(hdf['imgs']):
            plt.imsave(train_output+file.split("/")[-1]+"."+str(png_cntr) +".png",i)
            png_cntr+=1
    elif (case_id.split("-")[0] +"-"+ case_id.split("-")[1]+"-"+ case_id.split("-")[2]) in val_id:
        hdf = h5py.File(file)
        for i in list(hdf['imgs']):
            plt.imsave(val_output+file.split("/")[-1]+"."+str(png_cntr) +".png",i)
            png_cntr+=1  
      
    elif (case_id.split("-")[0] +"-"+ case_id.split("-")[1]+"-"+ case_id.split("-")[2]) in test_id:
        hdf = h5py.File(file)
        for i in list(hdf['imgs']):
            plt.imsave(test_output+file.split("/")[-1]+"."+str(png_cntr) +".png",i)
            png_cntr+=1

