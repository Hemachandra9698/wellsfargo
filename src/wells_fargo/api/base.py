

class DataSource:
    data_source_name = None  # type: Optional[str]

    def read_conf(self, conf_file):
        raise NotImplementedError("Method get_products() is not implemented.")

    def get_conf(self):
        raise NotImplementedError("Method get_conf() is not implemented.")

    def get_products_from_db(self, params):
        raise NotImplementedError("Method get_products_from_db() is not implemented.")

    def read_raw_data(self, params):
        raise NotImplementedError("Method read_raw_data() is not implemented.")

    def get_products(self):
        raise NotImplementedError("Method get_products() is not implemented.")

    def filter_data(self, data_df, filter_args):
        raise NotImplementedError("Method filter_data() is not implemented.")
