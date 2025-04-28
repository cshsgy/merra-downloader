import argparse
from config import Config
from downloader import MERRADownloader
from processor import MERRAProcessor
from products import MERRAProductCatalog

def main():
    parser = argparse.ArgumentParser(description="MERRA Data Downloader and Processor")
    parser.add_argument("--config", type=str, default="config.json", help="Path to configuration file")
    parser.add_argument("--output-dir", type=str, default="data", help="Directory to save downloaded files")
    parser.add_argument("--processed-dir", type=str, default="processed", help="Directory to save processed files")
    parser.add_argument("--list-products", action="store_true", help="List available products and exit")
    
    args = parser.parse_args()

    if args.list_products:
        print("Available MERRA Products:")
        for product_id, product in MERRAProductCatalog.list_products().items():
            print(f"\nProduct ID: {product_id}")
            print(f"Description: {product.description}")
            print(f"Frequency: {product.frequency}")
            print(f"Available Variables: {', '.join(product.variables)}")
        return

    # Initialize configuration
    config = Config(args.config)

    # Download data
    print("Starting download...")
    downloader = MERRADownloader(config)
    downloaded_files = downloader.download_data(args.output_dir)

    if not downloaded_files:
        print("No files were downloaded. Exiting.")
        return

    # Process downloaded files
    print("\nProcessing downloaded files...")
    processor = MERRAProcessor(config)
    processed_files = processor.process_files(downloaded_files, args.processed_dir)

    print(f"\nProcessing complete. {len(processed_files)} files were processed.")
    print(f"Processed files are saved in: {args.processed_dir}")

if __name__ == "__main__":
    main() 