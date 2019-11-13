# quality: gold
import copy
import os
import uuid

import pandas as pd

from source.data_model.dataset.Dataset import Dataset
from source.data_model.encoded_data.EncodedData import EncodedData
from source.data_model.repertoire.RepertoireGenerator import RepertoireGenerator


class RepertoireDataset(Dataset):

    def __init__(self, params: dict = None, encoded_data: EncodedData = None,
                 filenames: list = None, identifier: str = None, metadata_file: str = None):
        self.params = params
        self.encoded_data = encoded_data
        self.identifier = identifier if identifier is not None else uuid.uuid1()
        self._filenames = sorted(filenames) if filenames is not None else []
        self.metadata_file = metadata_file

    def add_encoded_data(self, encoded_data: EncodedData):
        self.encoded_data = encoded_data

    def get_data(self, batch_size: int = 1):
        self._filenames.sort()
        return RepertoireGenerator.build_item_generator(file_list=self._filenames, batch_size=batch_size)

    def get_batch(self, batch_size: int = 1):
        self._filenames.sort()
        return RepertoireGenerator.build_batch_generator(file_list=self._filenames, batch_size=batch_size)

    def get_repertoire(self, index: int = -1, filename: str = ""):
        assert index != -1 or filename != "", "RepertoireDataset: cannot load repertoire since the index nor filename are set."
        return RepertoireGenerator.load_repertoire(filename if filename != "" else self._filenames[index])

    def get_example_count(self):
        return len(self._filenames)

    def set_filenames(self, filenames: list):
        self._filenames = sorted(filenames)

    def get_filenames(self):
        return self._filenames

    def get_metadata(self, field_names: list, return_df: bool = False):
        df = pd.read_csv(self.metadata_file, sep=",", usecols=field_names)
        if return_df:
            return df
        else:
            return df.to_dict("list")

    def _build_new_metadata(self, indices, path) -> str:
        if self.metadata_file:
            df = pd.read_csv(self.metadata_file, index_col=0)
            df = df.iloc[indices, :]
            df.to_csv(path)
            return path
        else:
            return None

    def make_subset(self, example_indices, path):

        metadata_file = self._build_new_metadata(example_indices, path + "metadata.csv")
        new_dataset = RepertoireDataset(filenames=[self._filenames[i] for i in example_indices], params=copy.deepcopy(self.params),
                                        metadata_file=metadata_file)

        return new_dataset

    def get_repertoire_ids(self) -> list:
        if self.metadata_file and os.path.isfile(self.metadata_file):
            return pd.read_csv(self.metadata_file, usecols=["donor"], squeeze=True, dtype=str).values.tolist()
            # TODO: rename "donor" to "ID" everywhere (e.g. mixcr import) - standardize the names
        else:
            return [str(repertoire.identifier) for repertoire in self.get_data()]
