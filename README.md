# MP1 Data Pipeline

The things this pipeline can do include being able to process a CSV file, validate it, clean it, and save it.

In order to control it, use the config.yaml settings which is in the config/ folder: the config lists which columns are required or numeric, and lets you turn each cleaning step on or off(duplicates, missing values, outliers).

First, the pipeline checks that the input file and config file both exist. It then loads the CSV data and YAML config. Then the validator removes any rows that contain any invalid numbers and converts the column to numeric. Next, a copy is saved for the validated data that will show up later in the report and the processor does the rest of the processing such as removing duplicates, missing values and outliers. Finally, the pipeline saves the cleaned CSV and prints out a report that shows the before and after data and what it modified. During this whole process, should any steps fail, the program will exit with an error code of 1. 

The src/ folder is used for storing the backend programs such as data_loaders.py (loads the data), data_output.py (saves the data as a CSV file), data_processor.py (does all the lifting such as removing duplicates, outliers, processes the dataset, and creates a cleaning report summary), data_validator.py (checks for required_columns and numeric_columns), and utils.py (stores the setup_logging and validate_input functions), and the pipeline.py module connects all of the modules together.

The fixtures/ folder is basically demo samples of a CSV, JSON, YAML file that the program uses, and to be more clear, this pipeline can load CSV, JSON, and YAML files but ONLY can clean CSV files and the JSON and YAML files are there just to help load the data. 


## Usage

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

## Example output:

```
21:58:29 DEBUG    __main__ — Arguments parsed: input=fixtures/sample_data.csv, output=output/clean.csv
21:58:29 INFO     src.utils — Input file validated: fixtures/sample_data.csv
21:58:29 INFO     src.utils — Input file validated: config/config.yaml
21:58:29 INFO     src.data_loaders — Loaded CSV file: fixtures\sample_data.csv (100 rows)
21:58:29 INFO     src.data_loaders — Loaded YAML file: config\config.yaml
21:58:29 WARNING  src.data_validator — Invalid number value in rating: not_available
21:58:29 WARNING  src.data_validator — Invalid number value in rating: error
21:58:29 DEBUG    src.data_validator — Validation: 100 -> 98 rows 
21:58:29 INFO     __main__ — Validation complete: 100 -> 98 rows
21:58:29 DEBUG    src.data_processor — remove_duplicates: 98 -> 96 rows
21:58:29 DEBUG    src.data_processor — handle_missing: 96 -> 94 rows
21:58:29 DEBUG    src.data_processor — rating: method = iqr, threshold = 1.5, lower = 43.625, upper = 106.625, removed = 2
21:58:29 INFO     __main__ — Processing complete: 98 -> 92 rows
21:58:29 DEBUG    src.data_output — Saved 92 rows to output/clean.csv
21:58:29 INFO     __main__ — Saved cleaned data to output\clean.csv
Cleaning report:
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```