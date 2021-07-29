

# Deep Learning-based Frozen Section to FFPE Translation

<img src="imgs/overview.jpeg" width="800px"/>

### [Paper](https://arxiv.org/abs/2107.11786v1) | [Brain GBM Dataset](https://portal.gdc.cancer.gov/projects/TCGA-GBM) | [Brain LGG Dataset](https://portal.gdc.cancer.gov/projects/TCGA-LGG) | [Lung LUAD Dataset](https://portal.gdc.cancer.gov/projects/TCGA-LUAD) |  [Lung LUSC Dataset](https://portal.gdc.cancer.gov/projects/TCGA-LUSC) | [Pretrained Models](https://www.dropbox.com/sh/x7fvxx1fiohxwb4/AAAObJJTJpIHHi-s2UafrKeea?dl=0) | [WebSite](https://deepmia.boun.edu.tr/) 

In this work, we propose AI-FFPE pipeline which is optimized for histopathology images by driving the network attention specifically to the nuclei and tissue preperation protocols related deficiencies. Compared to [CycleGAN](https://github.com/junyanz/CycleGAN), our model training is faster and less memory-intensive.

<br>
<img src='imgs/frozgan_loss2.gif' align="right" width=960>
<br>

## Example Results

### Frozen to FFPE Translation in Brain Specimens
<img src="imgs/brain_gif.gif" width="800px"/>

### Frozen to FFPE Translation in Lung Specimens
<img src="imgs/lung_gif.gif" width="800px"/>


## Prerequisites
- Linux or macOS
- Python 3
- CPU or NVIDIA GPU + CUDA CuDNN


### Getting started

- Clone this repo:
```bash
git clone https://github.com/DeepMIALab/AI-FFPE
cd AI-FFPE
```

- Install PyTorch 1.1 and other dependencies (e.g., torchvision, visdom, dominate, gputil).

  For pip users, please type the command `pip install -r requirements.txt`.

  For Conda users,  you can create a new Conda environment using `conda env create -f environment.yml`.

### Training and Test

- Download the [Frozen_Brain](https://portal.gdc.cancer.gov/projects/TCGA-GBM) dataset (Fig. 3 of the paper. Frozen_Brain -> FFPE_BRAIN).
- Unzip the dataset at `./datasets/Frozen/Brain/`.
- Download the [Frozen_Lung](https://portal.gdc.cancer.gov/projects/TCGA-LUAD) dataset (Fig. 4 of the paper. Frozen_Lung -> FFPE_LUNG).
- Unzip the dataset at `./datasets/Frozen/Lung/`.

The data used for training are expected to be organized as follows:
```bash
Data_Path                # DIR_TO_TRAIN_DATASET
 ├──  trainA
 |      ├── 1.png     
 |      ├── ...
 |      └── n.png
 ├──  trainB     
 |      ├── 1.png     
 |      ├── ...
 |      └── m.png
 ├──  valA
 |      ├── 1.png     
 |      ├── ...
 |      └── k.png
 └──  valB     
        ├── 1.png     
        ├── ...
        └── l.png

```

- To view training results and loss plots, run `python -m visdom.server` and click the URL http://localhost:8097.

- Train the AI-FFPE model:
```bash
python train.py --dataroot ./datasets/${dataroot_dir_name} --name ${result_dir_name} --CUT_mode CUT --batch_size 1
```

- Test the AI-FFPE  model:
```bash
python test.py --dataroot ./datasets/Frozen/Lung  --name ${result_dir_name} --CUT_mode CUT --phase test --epoch ${epoch_number} --num_test ${number_of_test_images}
```

The test results will be saved to a html file here: "./results/${result_dir_name}/latest_train/index.html". 



### AI-FFPE, AI-FFPE without Spatial Attention Block, AI-FFPE without self-regularization loss, CUT, FastCUT, and CycleGAN

<img src="imgs/ablation.png" width="800px"/>

### Apply a pre-trained AI-FFPE model and evaluate

For reproducability, you can download the pretrained models for each algorithm [here.](https://www.dropbox.com/sh/x7fvxx1fiohxwb4/AAAObJJTJpIHHi-s2UafrKeea?dl=0)

## Reference

If you find our work useful in your research or if you use parts of this code please consider citing our paper:

```
@misc{ozyoruk2021frozen2ffpe,
      title={Deep Learning-based Frozen Section to FFPE Translation}, 
      author={ Kutsev Bengisu Ozyoruk, Sermet Can, Guliz Irem Gokceler, Kayhan Başak, Derya Demir, Gurdeniz Serin, Uguray Payam Hacisalihoglu, Berkan Darbaz,  Ming Y. Lu, Tiffany Y. Chen, Drew F. K. Williamson, Funda Yilmaz, Faisal Mahmood and Mehmet Turan},
      year={2021},
      eprint={2107.11786},
      archivePrefix={arXiv},
      primaryClass={cs.CV}
}
```



### Acknowledgments
Our code is developed based on [CUT](https://github.com/taesungp/contrastive-unpaired-translation). We also thank [pytorch-fid](https://github.com/mseitzer/pytorch-fid) for FID computation, and [stylegan2-pytorch](https://github.com/rosinality/stylegan2-pytorch/) for the PyTorch implementation of StyleGAN2 used in our single-image translation setting.
