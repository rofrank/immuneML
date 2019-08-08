from unittest import TestCase

from source.encodings.kmer_frequency.KmerFrequencyEncoder import KmerFrequencyEncoder
from source.encodings.word2vec.Word2VecEncoder import Word2VecEncoder
from source.hyperparameter_optimization.HPSetting import HPSetting
from source.hyperparameter_optimization.strategy.GridSearch import GridSearch
from source.ml_methods.SimpleLogisticRegression import SimpleLogisticRegression


class TestGridSearch(TestCase):
    def test_get_next_setting(self):

        hp_settings = [HPSetting(encoder=KmerFrequencyEncoder, encoder_params={}, ml_method=SimpleLogisticRegression(),
                                 ml_params={"model_selection_cv": False, "model_selection_n_fold": -1},
                                 preproc_sequence=[]),
                       HPSetting(encoder=Word2VecEncoder, encoder_params={}, ml_method=SimpleLogisticRegression(),
                                 ml_params={"model_selection_cv": False, "model_selection_n_fold": -1},
                                 preproc_sequence=[])]

        grid_search = GridSearch(hp_settings)
        setting1 = grid_search.get_next_setting()
        setting2 = grid_search.get_next_setting(setting1, {"label1": 0.7})
        setting3 = grid_search.get_next_setting(setting2, {"label1": 0.8})

        self.assertIsNone(setting3)
        self.assertEqual(KmerFrequencyEncoder, setting1.encoder)
        self.assertEqual(Word2VecEncoder, setting2.encoder)

    def test_get_optimal_hps(self):
        hp_settings = [HPSetting(encoder=KmerFrequencyEncoder, encoder_params={}, ml_method=SimpleLogisticRegression(),
                                 ml_params={"model_selection_cv": False, "model_selection_n_fold": -1},
                                 preproc_sequence=[]),
                       HPSetting(encoder=Word2VecEncoder, encoder_params={}, ml_method=SimpleLogisticRegression(),
                                 ml_params={"model_selection_cv": False, "model_selection_n_fold": -1},
                                 preproc_sequence=[])]

        grid_search = GridSearch(hp_settings)
        setting1 = grid_search.get_next_setting()
        setting2 = grid_search.get_next_setting(setting1, {"label1": 0.7})
        grid_search.get_next_setting(setting2, {"label1": 0.8})

        optimal = grid_search.get_optimal_hps()

        self.assertEqual(hp_settings[1], optimal)