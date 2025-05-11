import json
import logging
from datetime import datetime
from pathlib import Path

class DataSaver:
    def __init__(self, output_dir_base):
        self.output_dir_base = output_dir_base
        self.output_dir_base.mkdir(parents=True, exist_ok=True)
        self.logger = logging.getLogger('instagram_scraper.data_saver')

    def save_json(self, data, filename_prefix):
        date_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        output_path = self.output_dir_base / f"{filename_prefix}_{date_str}.json"
        
        self.logger.info(f'Data saved: {output_path}')
        try:
            with open(output_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            self.logger.info(f'File sucesfully saved : {output_path}')
            return True
        except Exception as e:
            self.logger.error(f'JSON failed: {e}')
            return False