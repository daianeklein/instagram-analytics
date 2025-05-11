import logging

class ApifyService:
    def __init__(self, client, actor_id):
        self.client = client
        self.actor_id = actor_id
        self.logger = logging.getLogger('instagram_scraper.apify')

    def run_actor(self, username, result_limit):
        run_input = {'username': [username],
                     'resultsLimit': result_limit}
        
        self.logger.info(f"Executando ator para buscar dados de: {username}")
        try:
            run = self.client.actor(self.actor_id).call(run_input=run_input)
            return run
        except Exception as e:
            self.logger.error(f'Falha ao executar o ator do Apify: {e}')
            return None
        
    def fetch_dataset_items(self, dataset_id):
        self.logger.info(f"Buscando itens do dataset: {dataset_id}")
        try:
            return list(self.client.dataset(dataset_id).iterate_items())
        except Exception as e:
            self.logger.error(f'Erro ao buscar itens do dataset: {e}')
            return []