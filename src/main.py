import sys
from pathlib import Path

# Add src directory to Python path
current_path = Path(__file__).resolve()
src_dir = current_path.parent
sys.path.insert(0, str(src_dir))

print(src_dir)

# Import modules
from api import get_posts
from transform import transform_instagram_results

def instagram_data_pipeline(profile: str):
    """
    Execute full Instagram data pipeline.
    """
    # Fetch posts
    raw_json_path = get_posts.fetch_and_save_posts(profile)
    
    # Process data
    processed_csv_path = raw_json_path.parent.parent / 'processed' / f'{raw_json_path.stem}_processed.csv'
    transform_instagram_results.process_instagram_data(raw_json_path, processed_csv_path)
    
    return raw_json_path, processed_csv_path

def main():
    """
    Main function to run Instagram data pipeline.
    Supports command-line argument or interactive input.
    """
    # Check for command-line argument
    if len(sys.argv) > 1:
        profile = sys.argv[1]
    else:
        # Interactive input
        profile = input("Enter Instagram profile to process: ").strip()
    try:
        raw_file, processed_file = instagram_data_pipeline(profile)
        
        print("\nPipeline completed successfully:")
        print(f"Raw data: {raw_file}")
        print(f"Processed data: {processed_file}")
    
    except Exception as e:
        print(f"An error occurred during the pipeline: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()