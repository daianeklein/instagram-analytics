from apify_client import ApifyClient
from config import Config
from logging_setup import setup_logging
from services.apify_service import ApifyService
from utils.data_saver import DataSaver
from domain.instagram_fetcher import InstagramDataFetcher

def main():
    """Função principal que orquestra o fluxo da aplicação."""
    # Configura o logging
    logger = setup_logging()
    logger.info("Iniciando aplicação")
    
    try:
        # Carrega e valida configurações
        config = Config()
        config.validate()
        
        # Inicializa os serviços
        apify_client = ApifyClient(config.api_key)
        apify_service = ApifyService(apify_client, config.actor_id)
        data_saver = DataSaver(config.output_dir_base)
        
        # Busca e salva os dados
        instagram_fetcher = InstagramDataFetcher(
            apify_service, 
            data_saver, 
            config.default_username, 
            config.default_result_limit
        )
        success = instagram_fetcher.fetch_and_save()
        
        if success:
            logger.info("Processo concluído com sucesso")
        else:
            logger.warning("Processo concluído com avisos ou erros")
            
    except Exception as e:
        logger.exception(f"Erro fatal na aplicação: {e}")
        
    logger.info("Encerrando aplicação")

if __name__ == '__main__':
    main()