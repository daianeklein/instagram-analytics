import logging

class InstagramDataFetcher:    
    def __init__(self, apify_service, data_saver, username, result_limit):
        self.apify_service = apify_service
        self.data_saver = data_saver
        self.username = username
        self.result_limit = result_limit
        self.logger = logging.getLogger('instagram_scraper.fetcher')

    def fetch_and_save(self):
        self.logger.info(f"Iniciando a busca de dados para o usuário: {self.username}")
        
        # Executa o ator do Apify
        run = self.apify_service.run_actor(self.username, self.result_limit)
        if not run or 'defaultDatasetId' not in run:
            self.logger.error(f"Falha ao executar o ator ou obter o ID do dataset para: {self.username}")
            return False
        
        # Busca os dados do dataset
        data = self.apify_service.fetch_dataset_items(run['defaultDatasetId'])
        if not data:
            self.logger.warning(f"Nenhum dado encontrado para o usuário: {self.username}")
            return False
        
        # Salva os dados em arquivo
        if self.data_saver.save_json(data, f"instagram_{self.username}"):
            self.logger.info(f"Dados de {self.username} coletados e salvos com sucesso.")
            return True
        else:
            self.logger.error(f"Falha ao salvar os dados de {self.username} para JSON.")
            return False