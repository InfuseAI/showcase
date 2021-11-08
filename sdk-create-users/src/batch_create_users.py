import json
import pandas as pd
from primehub import PrimeHub, PrimeHubConfig


class BatchCreateUsers:
    def __init__(self, primehub_cluster_url, bool_primehub_config):
        self.ph = None
        self.__init_primehub(primehub_cluster_url, bool_primehub_config)

    def __init_primehub(self, primehub_cluster_url, bool_primehub_config):
        self.ph = PrimeHub(PrimeHubConfig())
        if bool_primehub_config:
            self.ph.config.generate(primehub_cluster_url)
        elif self.ph.is_ready():
            print("PrimeHub Python SDK setup successfully.")
        else:
            self.ph.config.generate(primehub_cluster_url)
    
    def batch_create_users(self, file_path):
        config_list = self._arrange_primehub_users(file_path)
        self._create_users(config_list)
        print("Finish creating users. Please check in PrimeHub admin portal.")
    
    def _arrange_primehub_users(self, file_path):
        config_list = []
        df = pd.read_csv(file_path)
        df.isAdmin = df.isAdmin.astype('bool')
        config_list = json.loads(df.to_json(orient="records"))
        return config_list

    def _create_users(self, config_list):
        for config in config_list:
            print(config)
            self.ph.admin.users.create(config)
