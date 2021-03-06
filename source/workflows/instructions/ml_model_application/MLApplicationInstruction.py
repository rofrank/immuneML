import pandas as pd

from source.data_model.dataset.Dataset import Dataset
from source.environment.LabelConfiguration import LabelConfiguration
from source.hyperparameter_optimization.HPSetting import HPSetting
from source.hyperparameter_optimization.core.HPUtil import HPUtil
from source.util.PathBuilder import PathBuilder
from source.workflows.instructions.Instruction import Instruction
from source.workflows.instructions.ml_model_application.MLApplicationState import MLApplicationState


class MLApplicationInstruction(Instruction):
    """
    Instruction which enables using trained ML models and encoders on new datasets which do not necessarily have labeled data.

    The predictions are stored in the predictions.csv in the result path in the following format:


    .. list-table::
        :widths: 25 25 25 25
        :header-rows: 1

        * - example_id
          - cmv
          - cmv_true_proba
          - cmv_false_proba
        * - e1
          - True
          - 0.8
          - 0.2
        * - e2
          - False
          - 0.2
          - 0.8
        * - e3
          - True
          - 0.78
          - 0.22

    Arguments:

        dataset: dataset for which examples need to be classified

        label: name of the label that should be predicted (e.g., CMV, celiac_disease)

        config_path: path to the zip file exported from MLModelTraining instruction (which includes train ML model, encoder, preprocessing etc.)

        pool_size (int): number of processes to use for prediction

        store_encoded_data (bool): whether encoded dataset should be stored on disk; can be True or False; setting this argument to True might
        increase the disk space usage

    Specification example for the MLApplication instruction:

    .. highlight:: yaml
    .. code-block:: yaml

        instruction_name:
            type: MLApplication
            dataset: d1
            config_path: ./config.zip
            pool_size: 1000
            label: CD
            store_encoded_data: False

    """

    def __init__(self, dataset: Dataset, label_configuration: LabelConfiguration, hp_setting: HPSetting, pool_size: int, name: str,
                 store_encoded_data: bool):

        self.state = MLApplicationState(dataset=dataset, hp_setting=hp_setting, label_config=label_configuration, pool_size=pool_size, name=name,
                                        store_encoded_data=store_encoded_data)

    def run(self, result_path: str):
        self.state.path = PathBuilder.build(f"{result_path}/{self.state.name}/")

        dataset = self.state.dataset

        if self.state.hp_setting.preproc_sequence is not None:
            dataset = HPUtil.preprocess_dataset(dataset, self.state.hp_setting.preproc_sequence, self.state.path)

        dataset = HPUtil.encode_dataset(dataset, self.state.hp_setting, self.state.path, learn_model=False, number_of_processes=self.state.pool_size,
                                        label_configuration=self.state.label_config, context={}, encode_labels=False,
                                        store_encoded_data=self.state.store_encoded_data)

        self._make_predictions(dataset)

        return self.state

    def _make_predictions(self, dataset):

        label = self.state.label_config.get_labels_by_name()[0]

        method = self.state.hp_setting.ml_method
        predictions = method.predict(dataset.encoded_data, label)
        predictions_df = pd.DataFrame({"example_id": dataset.get_example_ids(), label: predictions[label]})

        if method.can_predict_proba():
            classes = method.get_classes_for_label(label)
            predictions_proba = method.predict_proba(dataset.encoded_data, label)[label]
            for cls_index, cls in enumerate(classes):
                predictions_df[f'{label}_{cls}_proba'] = predictions_proba[:, cls_index]

        self.state.predictions_path = self.state.path + "predictions.csv"
        predictions_df.to_csv(self.state.predictions_path, index=False)
