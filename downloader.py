import requests
from typing import List, Dict, Any
import datetime
import os
from config import Config

class MERRADownloader:
    def __init__(self, config: Config):
        self.config = config
        self.username, self.password = config.get_credentials()
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)

    def _generate_file_urls(self, product_id: str, start_date: str, end_date: str) -> List[str]:
        """Generate list of file URLs for the given date range."""
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        
        urls = []
        current = start
        while current <= end:
            year = current.year
            month = current.month
            day = current.day
            
            # Format URL based on product type
            if "M2I3N" in product_id:  # 3-hourly products
                for hour in range(0, 24, 3):
                    url = f"{self.config.base_url}{product_id}/{year}/{month:02d}/MERRA2_400.{product_id}.{year}{month:02d}{day:02d}.{hour:02d}00.nc4"
                    urls.append(url)
            elif "M2T1N" in product_id:  # 1-hourly products
                for hour in range(24):
                    url = f"{self.config.base_url}{product_id}/{year}/{month:02d}/MERRA2_400.{product_id}.{year}{month:02d}{day:02d}.{hour:02d}00.nc4"
                    urls.append(url)
            elif "M2TMN" in product_id:  # Monthly products
                url = f"{self.config.base_url}{product_id}/{year}/{month:02d}/MERRA2_400.{product_id}.{year}{month:02d}.nc4"
                urls.append(url)
            
            current += datetime.timedelta(days=1)
        
        return urls

    def download_data(self, output_dir: str = "data") -> List[str]:
        """Download MERRA data based on configuration."""
        config = self.config.config
        product_id = config["product"]
        start_date = config["time_range"]["start"]
        end_date = config["time_range"]["end"]
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate file URLs
        urls = self._generate_file_urls(product_id, start_date, end_date)
        
        downloaded_files = []
        for url in urls:
            try:
                response = self.session.get(url)
                response.raise_for_status()
                
                # Extract filename from URL
                filename = url.split("/")[-1]
                filepath = os.path.join(output_dir, filename)
                
                # Save the file
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                downloaded_files.append(filepath)
                print(f"Downloaded: {filename}")
                
            except requests.exceptions.RequestException as e:
                print(f"Error downloading {url}: {str(e)}")
        
        return downloaded_files 