import os
from pathlib import Path
from dotenv import load_dotenv

class Config:
    def __init__(self, env_file='.env'):
        load_dotenv(env_file)
        
        # API setup
        self.api_key = os.getenv('API_APIFY')
        self.actor_id = os.getenv('ACTOR_ID')
        
        self.default_username = os.getenv('DEFAULT_USERNAME', 'ladygaga')
        self.default_result_limit = int(os.getenv('DEFAULT_RESULT_LIMIT', '1'))
        
        # Dirs
        self.base_dir = Path.cwd().parent.parent
        self.output_dir_base = self.base_dir / os.getenv('OUTPUT_DIR', 'data/raw')
        
        self.output_dir_base.mkdir(parents=True, exist_ok=True)

    def validate(self):
        if not self.api_key:
            raise ValueError("A variável de ambiente API_APIFY deve estar definida.")
        if not self.actor_id:
            raise ValueError("A variável de ambiente ACTOR_ID deve estar definida.")
        return True