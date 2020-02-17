import datetime
import json
class Config:

    def __init__(self, json_file_path):
        with open(json_file_path) as json_file:
            json_config = json.load(json_file)
        self.min_num_of_authors = json_config['min_num_of_authors']
        self.max_num_of_authors = json_config['max_num_of_authors']
        self.max_num_of_windows = json_config['max_num_of_windows']
        self.min_num_of_windows = json_config['min_num_of_windows']
        self.time_period_begin = datetime.datetime(int(json_config['time_period_begin_year']),1,1)
        self.time_period_end = datetime.datetime(int(json_config['time_period_end_year']),12,31)
        self.input_folder = json_config['input_folder']
        self.output_folder = json_config['output_folder']
        self.output_doc_num = json_config['output_doc_num']
        self.seed = json_config['seed']
        self.window_size = json_config['window_size']
        self.allow_window_variation = json_config['allow_window_variation']
        self.variation_scaling_factor = json_config['variation_scaling_factor']