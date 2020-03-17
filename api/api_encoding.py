import glob
import os
import random

import pandas as pd

from source.IO.dataset_import.MiXCRLoader import MiXCRLoader
from source.encodings.EncoderParams import EncoderParams
from source.encodings.kmer_frequency.KmerFrequencyEncoder import KmerFrequencyEncoder
from source.environment.Label import Label
from source.environment.LabelConfiguration import LabelConfiguration
from source.reports.encoding_reports.DesignMatrixExporter import DesignMatrixExporter
from source.util.PathBuilder import PathBuilder
from source.workflows.steps.DataEncoder import DataEncoder
from source.workflows.steps.DataEncoderParams import DataEncoderParams


def encode_dataset_by_kmer_freq(path_to_dataset_directory: str, result_path: str, metadata_path: str = None):
    if metadata_path is None:
        metadata_path = generate_random_metadata(path_to_dataset_directory, result_path)

    loader = MiXCRLoader()
    dataset = loader.load(path_to_dataset_directory, {
        'metadata_file': metadata_path,
        "sequence_type": "CDR3",  # load in only cdr3
        "batch_size": 4,  # number of parallel processes for loading the data
        "result_path": result_path,
        "extension": "tsv",
        "CDR3_type": "IMGT"  # which CDR3 definition to use - IMGT here (will remove first and last a.a. compared to IMGT junction)
    })

    label_name = list(dataset.params.keys())[0]  # label that can be used for ML prediction - by default: "disease" with values True/False

    encoded_dataset = DataEncoder.run(DataEncoderParams(dataset, KmerFrequencyEncoder.build_object(dataset, **{
        "normalization_type": "relative_frequency",  # encode repertoire by the relative frequency of k-mers in repertoire
        "reads": "unique",  # count each sequence only once, do not use clonal count
        "k": 2,  # k-mer length
        "sequence_encoding": "continuous_kmer"  # split each sequence in repertoire to overlapping k-mers
    }), EncoderParams(result_path=result_path,
                      label_configuration=LabelConfiguration([Label(label_name, dataset.params[label_name])]),
                      filename="encoded_dataset.pickle")))

    dataset_exporter = DesignMatrixExporter(dataset=encoded_dataset,
                                            result_path=f"{result_path if result_path[:-1] == '/' else result_path+'/'}csv_exported/")
    dataset_exporter.generate_report()

    return encoded_dataset


def generate_random_metadata(path_to_dataset_directory: str, result_path: str):

    path_to_dataset_directory = path_to_dataset_directory if path_to_dataset_directory[:-1] == '/' else f"{path_to_dataset_directory}/"
    repertoire_filenames = list(glob.glob(f"{path_to_dataset_directory}*"))
    repertoire_count = len(repertoire_filenames)

    df = pd.DataFrame({"filename": [os.path.basename(filename) for filename in repertoire_filenames],
                       "disease": [random.choice([True, False]) for i in range(repertoire_count)],
                       "donor": [str(i) for i in range(1, repertoire_count + 1)]})

    PathBuilder.build(result_path)
    metadata_path = f"{result_path if result_path[:-1] == '/' else result_path+'/'}metadata.csv"
    df.to_csv(metadata_path, index=None)

    return metadata_path