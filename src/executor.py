from src.config import Config
import preprocess_NLP_pkg
from src.AuthorCollection import AuthorCollection
import datetime
from src.generator import generate_dataset
from pathlib import Path


config = Config('src/config.json')
input_folder = "/Users/sukanyanath/Documents/PhD/Datasets/Gutenberg_Adventure/"
output_folder = "/Users/sukanyanath/Documents/PhD/Datasets/Gutenberg_Adventure_output"

Path(output_folder).mkdir(parents=True, exist_ok=True)
author_collection = AuthorCollection(config.input_folder)
author_collection.filter_author_with_period(start_date=config.time_period_begin,end_date=config.time_period_end)
generate_dataset(author_collection=author_collection,
                 output_folder=config.output_folder,
                 output_doc_num=config.output_doc_num,
                 min_num_of_authors=config.min_num_of_authors,
                 max_num_of_authors=config.max_num_of_authors,
                 min_num_of_windows=config.min_num_of_windows,
                 max_num_of_windows=config.max_num_of_windows,
                 seed = config.seed,
                 window_size=config.window_size,
                 allow_window_variation=config.allow_window_variation,
                 variation_scaling_factor=config.variation_scaling_factor)



