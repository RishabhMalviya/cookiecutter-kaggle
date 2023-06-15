import os


_curr_dir = os.path.dirname(os.path.abspath(__file__))

RAW_DATA_DIR = os.path.join(_curr_dir, '../data/1_raw')
INTERMEDIATE_DATA_DIR = os.path.join(_curr_dir, '../data/2_intermediate')
PROCESSED_DATA_DIR = os.path.join(_curr_dir, '../data/3_processed')

EXPERIMENT_LOGS_DIR = os.path.join(_curr_dir, '../experiments/logs')
