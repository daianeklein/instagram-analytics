import logging
from datetime import datetime

def setup_logging(level=logging.INFO):
    """
    Configura o sistema de logging da aplicação.
    
    Args:
        level: Nível de log desejado
    """
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),  # Saída para console
            logging.FileHandler(f"instagram_scraper_{datetime.now().strftime('%Y-%m-%d')}.log")  # Saída para arquivo
        ]
    )
    return logging.getLogger('instagram_scraper')
