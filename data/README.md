# Input & Output

* All the input files needs to be stored into `input` directory.
* All the output files will be generated into `output` directory.
* Any file that needs to be used as an input or generated to be as output we have to include them into the `catalog.yml` file.
* Please refer to the example for better understanding.
* When stored we have to provide the `file_path` in the `catalog.yml` along with a name.
This name is referred as dataframe file by Kedro automatically.
* Kedro checks for `node` in `src/<project-name>/pipelines/<pipeline-name>/pipeline.py'.
* If any node specifies a param `inputs` and contains the `name` matches in the `catalog.yml` file, it considers as `input` and loads the data automatically in the `type` we have provided.

```
 Input example where file exists in the given path:
    sample_data1:
      type: pandas.CSVDataSet
      filepath: data/input/data_source_1/sample_data.1.csv
      load_args:
        sep: ","
      save_args:
        index: False
        date_format: "%Y-%m-%d %H:%M"
```
* This tells to read the `sample_data.1.csv` from the given `file_path` and name it as `sample_data1`
* The type it reads as `CSVDataSet`
* While loading the data we have also provided few `load_args`, here, `sep:','`
* This tells Kedro to read this data and use the delimiter as a comma. `,`
* Similarly we do have `save_args` that tells Kedro to use them when saving the file.
* `index` tells Kedro to be inserted if `True`.
* `date_format` tells Kedro to format the date columns in the dataframe while saving.

```
Output example where file not exists in the given path:
consolidated_data1:
  type: pandas.CSVDataSet
  filepath: data/output/consolidated_output.1.csv
  load_args:
    sep: ","
  save_args:
    index: False
    date_format: "%Y-%m-%d %H:%M"
```
* For output, Kedro scans the `src/<project-name>/pipelines/<pipeline-name>/pipeline.py'
* It checks for the param `outputs` and matches it with the name specified in the `catalog.yml` -> here it is `consolidated_data1`
* If it matches when the `node` runs it stores the output generated as specified in the `catalog.yml` file.