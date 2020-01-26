from unittest import TestCase
import os
import pandas as pd

from source.data_model.dataset.RepertoireDataset import RepertoireDataset
from source.encodings.word2vec.Word2VecEncoder import Word2VecEncoder
from source.encodings.word2vec.model_creator.ModelType import ModelType
from source.environment.EnvironmentSettings import EnvironmentSettings
from source.environment.Label import Label
from source.environment.LabelConfiguration import LabelConfiguration
from source.environment.MetricType import MetricType
from source.hyperparameter_optimization.HPSetting import HPSetting
from source.hyperparameter_optimization.config.SplitConfig import SplitConfig
from source.hyperparameter_optimization.config.SplitType import SplitType
from source.hyperparameter_optimization.strategy.GridSearch import GridSearch
from source.ml_methods.SimpleLogisticRegression import SimpleLogisticRegression
from source.reports.ml_reports.BenchmarkHPSettings import BenchmarkHPSettings
from source.util.PathBuilder import PathBuilder
from source.util.RepertoireBuilder import RepertoireBuilder
from source.workflows.instructions.HPOptimizationInstruction import HPOptimizationInstruction
from source.dsl.report_params_parsers.ErrorBarMeaning import ErrorBarMeaning


class TestBenchmarkHPSettings(TestCase):

    def _create_state_object(self, path):
        repertoires, metadata = RepertoireBuilder.build(sequences=[["AAA", "CCC", "DDD"], ["AAA", "CCC", "DDD"],
                                                                   ["AAA", "CCC", "DDD"], ["AAA", "CCC", "DDD"],
                                                                   ["AAA", "CCC", "DDD"], ["AAA", "CCC", "DDD"],
                                                                   ["AAA", "CCC", "DDD"], ["AAA", "CCC", "DDD"],
                                                                   ["AAA", "CCC", "DDD"], ["AAA", "CCC", "DDD"],
                                                                   ["AAA", "CCC", "DDD"], ["AAA", "CCC", "DDD"],
                                                                   ["AAA", "CCC", "DDD"], ["AAA", "CCC", "DDD"],
                                                                   ["AAA", "CCC", "DDD"], ["AAA", "CCC", "DDD"],
                                                                   ["AAA", "CCC", "DDD"], ["AAA", "CCC", "DDD"],
                                                                   ["AAA", "CCC", "DDD"], ["AAA", "CCC", "DDD"],
                                                                   ["AAA", "CCC", "DDD"], ["AAA", "CCC", "DDD"],
                                                                   ["AAA", "CCC", "DDD"], ["AAA", "CCC", "DDD"],
                                                                   ["AAA", "CCC", "DDD"], ["AAA", "CCC", "DDD"],
                                                                   ["AAA", "CCC", "DDD"], ["AAA", "CCC", "DDD"],
                                                                   ["AAA", "CCC", "DDD"], ["AAA", "CCC", "DDD"],
                                                                   ["AAA", "CCC", "DDD"], ["AAA", "CCC", "DDD"],
                                                                   ["AAA", "CCC", "DDD"], ["AAA", "CCC", "DDD"]],
                                                        path=path,
                                                        labels={
                                                            "l1": [1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2,
                                                                   1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2, 1, 2],
                                                            "l2": [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1,
                                                                   0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]})

        dataset = RepertoireDataset(repertoires=repertoires, metadata_file=metadata,
                                    params={"l1": [1, 2], "l2": [0, 1]})
        hp_settings = [HPSetting(Word2VecEncoder, {"k": 3, "model_type": ModelType.SEQUENCE, "vector_size": 4},
                                 SimpleLogisticRegression(),
                                 {"model_selection_cv": False, "model_selection_n_folds": -1},
                                 [])]

        label_config = LabelConfiguration([Label("l1", [1, 2]), Label("l2", [0, 1])])

        process = HPOptimizationInstruction(dataset, GridSearch(hp_settings), hp_settings,
                                            SplitConfig(SplitType.RANDOM, 1, 0.5),
                                            SplitConfig(SplitType.RANDOM, 1, 0.5),
                                            {MetricType.BALANCED_ACCURACY}, label_config, path)

        state = process.run(result_path=path)

        return state

    def test_generate(self):
        path = EnvironmentSettings.root_path + "test/tmp/benchmarkhpsettings/"
        PathBuilder.build(path)

        report = BenchmarkHPSettings(errorbar_meaning=ErrorBarMeaning.STANDARD_ERROR)


        report.result_path = path
        report.hp_optimization_state = self._create_state_object(path + "input_data/")

        report.check_prerequisites()
        report.generate()


        self.assertTrue(os.path.isfile(path + "benchmark_result.csv"))
        self.assertTrue(os.path.isfile(path + "benchmark_result.pdf"))

        written_data = pd.read_csv(path + "benchmark_result.csv")
        self.assertEqual(list(written_data.columns), ["fold", "label", "encoding", "ml_method", "performance"])
