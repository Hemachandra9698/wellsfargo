import os

from flask import Flask, request, render_template, render_template_string
from wells_fargo.api.parse_command_args import parse_arguments
from wells_fargo.api.rest import RestDataSource

# GLOBALS
rest_obj = RestDataSource()
BASE_DIR = os.path.normpath(os.getcwd() + "/../..") + '/'
TEMPLATES_DIR = BASE_DIR + 'templates/'
app = Flask(__name__, template_folder=TEMPLATES_DIR)


def get_filter_args():
    filter_args = {}
    filter_col_name = request.args.get('col_name')
    filter_col_val = request.args.get('col_val')
    if filter_col_name and filter_col_val:
        filter_args['filter_col_name'] = filter_col_name
        filter_args['filter_col_val'] = filter_col_val
    return filter_args


@app.route("/")
def index():
    filter_args = get_filter_args()
    products_df = rest_obj.get_products()
    if not products_df.empty and filter_args:
        filtered_products_df = rest_obj.filter_data(products_df, filter_args)
        if filtered_products_df.empty:
            return render_template_string('<b><h2>No values found in the products for {} with value: {}</h2></b>'.format(
                filter_args['filter_col_name'],
                filter_args['filter_col_val']
            ))
        return render_template_string(filtered_products_df.to_html())
    return render_template('products_not_found.html')


def main():
    """
    runs the flask server on the provided host and port
    :return:
    """
    command_args = parse_arguments()
    app.run(host=command_args.host, port=command_args.port, debug=True)


if __name__ == "__main__":
    main()