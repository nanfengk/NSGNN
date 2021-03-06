import warnings
from scipy.sparse import SparseEfficiencyWarning
warnings.simplefilter('ignore', SparseEfficiencyWarning)
from utils import *
import scipy.io as sio
import torch
from torch_geometric.data import InMemoryDataset
from torch_geometric.data import Data

class MyOwnDataset(InMemoryDataset):
    def __init__(self, root, transform=None, pre_transform=None):
        super().__init__(root, transform, pre_transform)
        self.data, self.slices = torch.load(self.processed_paths[0])

    @property
    def raw_file_names(self):
        return ['some_file_1', 'some_file_2', ...]

    @property
    def processed_file_names(self):
        return ['data.pt']

    def process(self):
        row_data = sio.loadmat('..\\raw_dataset\\DNdataset.mat')
        dis_drug_matrix = row_data['didr']
        drug_sim = row_data['drug']
        dis_sim = row_data['disease']
        num_di = dis_drug_matrix.shape[0]
        num_dr = dis_drug_matrix.shape[1]
        index_di = np.where(dis_drug_matrix)[0]
        index_dr = np.where(dis_drug_matrix)[1]
        index_dr = index_dr + num_di * np.ones((index_di.shape[0],), dtype=int)

        max_dr = index_dr[np.argmax(index_dr)]
        min_dr = index_dr[np.argmin(index_dr)]
        max_di = index_di[np.argmax(index_di)]
        min_di = index_di[np.argmin(index_di)]

        edge_index = torch.tensor([index_di, index_dr], dtype=torch.long)

        mat1 = np.hstack((dis_sim, np.zeros((num_di, num_dr))))

        mat2 = np.hstack((np.zeros((num_di, num_dr)).T, drug_sim))

        x = torch.tensor(np.vstack((mat1, mat2)))

        data = Data(x=x, edge_index=edge_index, num_nodes=max(max_di, max_dr) + 1, max_dr=max_dr,
                    min_dr=min_dr, max_di=max_di, min_di=min_di, dis_drug_matrix=dis_drug_matrix,
                    drug_sim=drug_sim, dis_sim=dis_sim, num_dr=num_dr, num_di=num_di)

        data_list = [data]

        if self.pre_filter is not None:
            data_list = [data for data in data_list if self.pre_filter(data)]

        if self.pre_transform is not None:
            data_list = [self.pre_transform(data) for data in data_list]

        data, slices = self.collate(data_list)
        torch.save((data, slices), self.processed_paths[0])
