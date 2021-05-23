# 怎么运行？

### Step 1：数据准备

下载HPA数据，并放到 /input/hpa-single-cell-image-classification 下。

下载训练集Cell Mask(https://www.kaggle.com/its7171/hpa-mask)放到 /input/hpa-mask/train 下。

* 对于公开数据集，需要运行/code/HPA-Cell-Segmentation/cell_mask.ipynb生成细胞分割图。



### Step 2：安装依赖

按照要求安装Cell Segmentation依赖。(https://github.com/CellProfiling/HPA-Cell-Segmentation)

repo已经clone到 /code/ 里了。



### Step 3：获得测试集合Mask

运行 /code/HPA-Cell-Segmentation/cell_mask.ipynb 获得测试集Cell Mask。



### Step 4：训练数据生成

运行 /code/cell_extract.ipynb 提取训练集和测试集的单细胞图像。

* 对于整图，仅使用RGB通道，并缩放至1024*1024尺寸（Repo中不包含此部分代码）。
* 可以根据绿色通道Max值重新分配细胞为类别18标签（Repo中不包含此部分代码）。



### Step 5：多标签分类训练

运行 /code/classification-fastai.ipynb 多标签分类训练，并生成单细胞预测结果。

* 对于不同模型和整图模型，需修改部分内容：模型类别、归一化的均值与方差、训练尺寸。



### Step 6：结果生成

运行 /code/generate_submission.ipynb 按照要求格式获得提交结果。



### Step 7：结果提交

结果提交。



## Tools

* /code/kaggle_submission.py

  用于本地生成结果并提交。

* /code/download_hpapublic.py

  下载public dataset，但是比赛方提供的数据及其混乱，为节约时间，本文件下载的为jpg格式文件，而非原始分辨率文件。

  你可以参考：

  https://www.kaggle.com/lnhtrang/hpa-public-data-download-and-hpacellseg

  https://www.kaggle.com/c/hpa-single-cell-image-classification/discussion/217021#1219554

  https://www.kaggle.com/philculliton/hpa-challenge-2021-extra-train-images

  简单来说，官方提供的包括三部分：

  * tif.gz 原分辨率图像（官方demo下载下来为16位图像，保存为8位图像）
  * jpg 图像
  * 并非全集的 png 图像 dataset

  另外，第一届比赛提供的HPAv18公开数据集约有78000张，目前提供的HPAPublic数据量约为80000张，交集为70000张。第一届的训练集也可以使用。

  总结一下，目前可用的数据集包括：

  * 本届正式训练集
  * 本届公开数据集
  * 上届训练集（与本届公开数据集有交集）
  * 上届公开数据集（与本届公开数据集有交集）

  

## Requirement

fastai： 2.2.5

