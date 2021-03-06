import os
import pickle
from typing import List, Tuple

from source.IO.ml_method.MLMethodConfiguration import MLMethodConfiguration
from source.environment.Label import Label
from source.hyperparameter_optimization.HPSetting import HPSetting
from source.preprocessing.Preprocessor import Preprocessor
from source.util.ReflectionHandler import ReflectionHandler


class MLImport:

    @staticmethod
    def import_encoder(config: MLMethodConfiguration, config_dir: str):
        encoder_class = ReflectionHandler.get_class_by_name(config.encoding_class)
        encoder = encoder_class.load_encoder(config_dir + config.encoding_file)
        return encoder

    @staticmethod
    def import_preprocessing_sequence(config: MLMethodConfiguration, config_dir) -> List[Preprocessor]:
        if os.path.isfile(config_dir + config.preprocessing_file):
            with open(config_dir + config.preprocessing_file, "rb") as file:
                preprocessing_sequence = pickle.load(file)
        else:
            preprocessing_sequence = []
        return preprocessing_sequence

    @staticmethod
    def import_hp_setting(config_dir: str) -> Tuple[HPSetting, Label]:

        config = MLMethodConfiguration()
        config.load(f'{config_dir}ml_config.yaml')

        ml_method = ReflectionHandler.get_class_by_name(config.ml_method, 'ml_methods/')()
        ml_method.load(config_dir)

        encoder = MLImport.import_encoder(config, config_dir)
        preprocessing_sequence = MLImport.import_preprocessing_sequence(config, config_dir)

        labels = list(config.labels_with_values.keys())
        assert len(labels) == 1, "MLImport: Multiple labels set in a single ml_config file."

        label = Label(labels[0], config.labels_with_values[labels[0]])

        return HPSetting(encoder=encoder, encoder_params=config.encoding_parameters, encoder_name=config.encoding_name,
                         ml_method=ml_method, ml_method_name=config.ml_method_name, ml_params={},
                         preproc_sequence=preprocessing_sequence, preproc_sequence_name=config.preprocessing_sequence_name), label
