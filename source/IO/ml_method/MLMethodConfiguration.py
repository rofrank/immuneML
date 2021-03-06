import os
from dataclasses import dataclass

import yaml

from source.util.PathBuilder import PathBuilder


@dataclass
class MLMethodConfiguration:

    labels_with_values: dict = None

    encoding_name: str = None
    encoding_class: str = None
    encoding_parameters: dict = None
    encoding_file: str = None

    preprocessing_sequence_name: str = None
    preprocessing_parameters: dict = None
    preprocessing_file: str = None

    ml_method: str = None
    ml_method_name: str = None

    train_dataset_id: str = None
    train_dataset_name: str = None
    software_used: str = None

    def store(self, path: str):
        PathBuilder.build(os.path.dirname(path))
        with open(path, "w") as file:
            yaml.dump(self.__dict__, file)

    def load(self, path: str):
        with open(path, 'r') as file:
            obj = yaml.load(file)
        self.__init__(**obj)
