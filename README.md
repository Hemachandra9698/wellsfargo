# wells-fargo

## Overview

This is your new Kedro project, which was generated using `Kedro 0.18.1`.

Take a look at the [Kedro documentation](https://kedro.readthedocs.io) to get started.
>>> Please refer to this documentation for a better understanding on how to start with Kedro and configure your project.

>>> I highly recommend to follow [these](https://kedro.readthedocs.io/en/stable/development/set_up_pycharm.html) to configure Pycharm with Kedro.
> There can be module errors while running from the terminal directly.

## Create a Virtual Environment
```
python -m venv .venv
.\.venv\scripts\activate
```
## How to install dependencies

Declare any dependencies in `src/requirements.txt` for `pip` installation and `src/environment.yml` for `conda` installation.

To install them, run:

```
pip install -r src/requirements.txt
```

## How to run your Kedro pipeline

You can run your Kedro project with:

```
kedro run
```

### IPython
And if you want to run an IPython session:

```
kedro ipython
```
### Configuration
All configuration for running the pipeline is parsed from:
```
conf/base/catalog.yml
conf/base/parameters/data_processing.yml
```
> NOTE: Please refer to README.md file in the /conf directory for better understanding on how to provide and update the inputs.

# Work Flow of Project
* The main code lies in `src/<project-name>/pipelines/<pipeline-name>pipeline.py`
* Kedro divides the Pipeline into multiple nodes. A `node` is a wrapper for the function that will be executed automatically by Kedro.
* The beauty of Kedro is it can able to run a single node by specifying `--node` while running the pipeline or if we don't pass the node param it 
runs all the nodes.
* Let's understand creating of node.
```
node(
     name='process_sample_data1_node',
     inputs=['sample_data1', 'parameters'],
     func=process_sample_data1,
     outputs='processed_sample_data1'
  )
```
* `node` contains `name, inputs, func, outputs` as mandatory parameters.
* `name` is a unique name given to the node. Using this we can tell Kedro to run only that node.
* `inputs` are the params passed to the function `process_sample_data1`.
    * `['sample_data1', 'parameters']` are the parameters being passed to the `func` which has the definition as follows:
    * ```
      def process_sample_data1(sample_data1, parameters):
          pass
      ```
    * The inputs can be anything, they can be normal strings or sometimes the values specified in the `catalog.yml` file present in `/conf` directory.
    * For example, we have specified an input with the name `sample_data1` in the `catalog.yml` file which actually tells Kedro to
  load it as a CSV file just as below:
    * ```
      sample_data1:
       type: pandas.CSVDataSet
       filepath: data/input/data_source_1/sample_data.1.csv
      ```
    * If you look above, we have specified `sample_data1` as a param which contains `file_path` as sub param to it.
    * If you observe the filepath value it specifies path to `sample_data.1.csv` file.
    * If you remember, in the above `node` we have given `inputs` as a list containing `sample_data1` as first element.
    * Whenever Kedro sees this, it automatically recognizes this as an input which needs to be loaded as the name is specified in `inputs` value in node.
    * `type` tells what is the data type in which Kedro has to load the CSV file. 
    * Finally, Kedro loads the CSV file automatically and assigns `sample_data1` name to it.

* `outputs` are the params that tells the function/node returns an output which has a name.
 Here it is `processed_sample_data1`. Whatever data the node `process_sample_data1_node` returns it will be assigned to the `outputs` name.
* If you specify the`processed_sample_data1` in the `catalog.yml` file then it automatically saves the file.
  * ```
    processed_sample_data1:
     type: pandas.CSVDataSet
     filepath: data/02_intermediate/processed_sample_data1.csv
    ```
  * As the `processed_sample_data1` is generated as an output by the node Kedro matches this with the name present in the `catalog.yml` file. If it founds there, it reads the `type` and 
   `filepath` parameters, saves the data into the path.
  * If we didn't specify `processed_sample_data1` in the `catalog.yml` file then Kedro stores it in memory.

* For more information on understanding nodes please visit:
>>> https://kedro.readthedocs.io/en/stable/get_started/hello_kedro.html#node

* Once we create a node Kedro calls the function specified in `func` param.
* The main logic is present in this function. What you want to do on the input that Kedro has read? What to generate or return? Where to save the generated data?
* You can also write a list of nodes and Kedro executes them Sequentially.
* We can pass a `node`'s output as an input to another node just by providing the `outputs` name of first node in
 `inputs` of the 2nd node.
* If there is no connection between the inputs and outputs from one node and another then we can also tell Kedro to run the nodes parallely.

# Solution for the task
* Once you download the project and followed all the steps till the  `Configuration` section navigate to the `project` directory. In our case it is `kedro-wf/wells-fargo`
* Just type `Kedro run`, if everything is smooth it executes without an error and generates 3 files.
```
data/output/consolidated_output.1.csv  -> contains final output
data/output/data2_aggregation_results.csv -> aggregation results for sample_data.2.csv
products_sqlite.db in the root dir -> contains the consolidated_output.1.csv records in sqlite db. 
```
* You could see the below output if your run is successful.

![Kedro Run Passed](images/run_passed.png?raw=true "Kedro Run Passed")

## Running Flask API for getting products.
>>> NOTE: Please run FLASK server once the Kedro run is successful if not the API returns an error message as 
> ''No Products found''
* For running the Flask server navigate and run the following command:
```
python src/wells_fargo/api/app.py
```
* The default port is 5001 and host is '0.0.0.0' but you can change it by providing the command line args as:
```
python src/wells_fargo/api/app.py -port 5001 -host 0.0.0.0
```
* Once the server is up, open below URL for getting all products.
```
http://127.0.0.1:5001/
```
![Get Products](images/products.png?raw=true "Products")

* For getting products which have product_name as `simple_thing`
```
http://127.0.0.1:5001/?col_name=product_name&col_val=simple_thing
```
>>> Send the column name as `col_name=<column_name>` and the value you want to match as
> `col_val=<column value>`

### Examples
```
http://127.0.0.1:5001/?col_name=material_id&col_val=2
http://127.0.0.1:5001/?col_name=worth&col_val=2
http://127.0.0.1:5001/?col_name=source&col_val=sample_data.2.dat
http://127.0.0.1:5001/?col_name=quality&col_val=low
```