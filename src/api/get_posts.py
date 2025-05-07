import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from apify_client import ApifyClient
from pathlib import Path

#logging config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ApifyService:
    def __init__(self, api_key, actor_id):
        self.client = ApifyClient(api_key)
        self.actor_id = actor_id

    def run_actor(self, username, result_limit):
        run_input = {'username' : [username],
                     'resultsLimit' : result_limit}
        
        try:
            run = self.client.actor(self.actor_id).call(run_input=run_input)
            return run
        except Exception as e:
            logging.error(f'APify Actor not run sucesfully: {e}')
            return None
        
    def fetch_dataset_items(self, dataset_id):
        try:
            return list(self.client.dataset(dataset_id).iterate_items())
        except Exception as e:
            logging.error(f'Error to fetch dataset items: {e}')
            return []

class DataSaver:
    def __init__(self, output_dir_base='data/raw'):
        self.output_dir_base = Path.cwd().parent.parent / output_dir_base
        self.output_dir_base.mkdir(parents=True, exist_ok=True)

    def save_json(self, data, filename_prefix):
        date_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_path = self.output_dir_base / f"{filename_prefix}_{date_str}.json"
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            logging.info(f'File saved: {output_path}')
            return True
        except Exception as e:
            logging.error(f'Saving JSON failed: {e}')
            return False

class InstagramDataFetcher:
    def __init__(self, apify_service, data_saver, username='ladygaga', result_limit=1):
        self.apify_service = apify_service
        self.data_saver = data_saver
        self.username = username
        self.result_limit = result_limit

    def fetch_and_save(self):
        logging.info(f"Iniciando a busca de dados para o usuário: {self.username}")
        run = self.apify_service.run_actor(self.username, self.result_limit)
        if run and 'defaultDatasetId' in run:
            data = self.apify_service.fetch_dataset_items(run['defaultDatasetId'])
            if data:
                if self.data_saver.save_json(data, f"instagram_{self.username}"):
                    logging.info(f"Dados de {self.username} coletados e salvos com sucesso.")
                else:
                    logging.error(f"Falha ao salvar os dados de {self.username} para JSON.")
            else:
                logging.warning(f"Nenhum dado encontrado para o usuário: {self.username}")
        else:
            logging.error(f"Falha ao executar o ator ou obter o ID do dataset para o usuário: {self.username}")

if __name__ == '__main__':
    load_dotenv()

    api_key = os.getenv('API_APIFY')
    actor_id = os.getenv('ACTOR_ID')

    if not api_key or not actor_id:
        logging.error("As variáveis de ambiente API_APIFY e ACTOR_ID devem estar definidas.")
    else:
        apify_service = ApifyService(api_key, actor_id)
        data_saver = DataSaver()
        instagram_fetcher = InstagramDataFetcher(apify_service, data_saver, username='ladygaga', result_limit=1)
        instagram_fetcher.fetch_and_save()