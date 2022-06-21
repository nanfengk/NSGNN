# NSGNN
## Paper "NSGNN： Predicting Drug-disease Associations Based on Neighborhood Subgraphs of Drug-disease Association Pairs"


### 'raw_dataset' directory
Contains Cdataset, DNdataset, Fdataset, LRSSL, Ndataset and detailed descriptions of each dataset

### 'dataset' directory
Raw drug-disease network data is processed to generate data for input into the NSGNN model

### 'results' directory
Metrics based on NSGNN models with five different datasets, including AUC, AUPR, F1 score, Accuracy, Recall, Specificity, Precision, MCC, etc.

### 'src' directory
1. Includes all source code for training NSGNN
2. To predict drug-disease associations by NSGNN, run

    ``` python
    python link_pred.py --dataset f_data --use_feature --epochs 100  --batch_size 32  --hidden_channels 256 --dropout 0.5
    ```

If you want to switch the generated dataset, we can do so by changing the 'dataset' in the sample.' use_feature' is used to control whether to use drug-drug similarity and disease-disease similarity matrix information. 'epochs', 'batch_size', 'hidden_channels' and ' dropout' are used to adjust the hyperparameters of the deep learning model.

