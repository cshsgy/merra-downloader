import requests
from typing import List, Dict, Any
import datetime
import os
from config import Config
import netCDF4 as nc
import numpy as np

class MERRADownloader:
    def __init__(self, config: Config):
        self.config = config
        self.username, self.password = config.get_credentials()
        self.session = requests.Session()
        self.session.auth = (self.username, self.password)

    def _get_product_info(self, product_id: str) -> tuple:
        """Get product information based on product ID."""
        # Map product IDs to their corresponding file name patterns
        product_id_main = product_id.split(".")[0]
        product_map = {
            "M2I3NPASM": ("inst3_3d_asm_Np", "3-hour"),
            "M2I3NVAER": ("inst3_3d_aer_Nv", "3-hour"),
            "M2T1NXFLX": ("tavg1_2d_flx_Nx", "1-hour"),
            "M2T1NXAER": ("tavg1_2d_aer_Nx", "1-hour"),
            "M2T1NXRAD": ("tavg1_2d_rad_Nx", "1-hour"),
            "M2TMNXAER": ("tavgM_2d_aer_Nx", "monthly"),
            "M2TMNXFLX": ("tavgM_2d_flx_Nx", "monthly"),
            "M2TMNXRAD": ("tavgM_2d_rad_Nx", "monthly")
        }
        
        if product_id_main not in product_map:
            raise ValueError(f"Unsupported product ID: {product_id_main}")
        
        return product_map[product_id_main]

    def _generate_file_urls(self, product_id: str, start_date: str, end_date: str) -> List[str]:
        """Generate list of file URLs for the given date range."""
        file_pattern, frequency = self._get_product_info(product_id)
        start = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.datetime.strptime(end_date, "%Y-%m-%d")
        
        urls = []
        current = start
        while current <= end:
            year = current.year
            month = current.month
            day = current.day
            
            if frequency == "3-hour":
                for hour in range(0, 24, 3):
                    filename = f"MERRA2_400.{file_pattern}.{year}{month:02d}{day:02d}.nc4"
                    url = f"{self.config.base_url}{product_id}/{year}/{month:02d}/{filename}"
                    urls.append(url)
            elif frequency == "1-hour":
                for hour in range(24):
                    filename = f"MERRA2_400.{file_pattern}.{year}{month:02d}{day:02d}.nc4"
                    url = f"{self.config.base_url}{product_id}/{year}/{month:02d}/{filename}"
                    urls.append(url)
            elif frequency == "monthly":
                filename = f"MERRA2_400.{file_pattern}.{year}{month:02d}.nc4"
                url = f"{self.config.base_url}{product_id}/{year}/{month:02d}/{filename}"
                urls.append(url)
            
            current += datetime.timedelta(days=1)
        
        return urls

    def _get_lat_lon_indices(self, dataset: nc.Dataset) -> tuple:
        """Get indices for the specified latitude-longitude box."""
        box = self.config.config["box"]
        lat = dataset.variables['lat'][:]
        lon = dataset.variables['lon'][:]
        
        lat_idx = np.where((lat >= box["south"]) & (lat <= box["north"]))[0]
        lon_idx = np.where((lon >= box["west"]) & (lon <= box["east"]))[0]
        
        return lat_idx, lon_idx

    def _get_subset_url(self, base_url: str, lat_idx: List[int], lon_idx: List[int], variables: List[str]) -> str:
        """Generate OpenDAP subset URL with specified variables and region."""
        # Convert indices to string ranges
        lat_range = f"[{min(lat_idx)}:1:{max(lat_idx)}]"
        lon_range = f"[{min(lon_idx)}:1:{max(lon_idx)}]"
        
        # Create variable subset string
        var_subset = ",".join([f"{var}{lat_range}{lon_range}" for var in variables])
        
        # Construct OpenDAP subset URL
        return f"{base_url}?{var_subset}"

    def download_data(self, output_dir: str = "data") -> List[str]:
        """Download MERRA data based on configuration."""
        config = self.config.config
        product_id = config["product"]
        start_date = config["time_range"]["start"]
        end_date = config["time_range"]["end"]
        variables = config["variables"]
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate file URLs
        urls = self._generate_file_urls(product_id, start_date, end_date)
        
        downloaded_files = []
        for url in urls:
            try:
                # First, get the dataset metadata to determine lat/lon indices
                with nc.Dataset(url) as ds:
                    lat_idx, lon_idx = self._get_lat_lon_indices(ds)
                
                # Generate subset URL
                subset_url = self._get_subset_url(url, lat_idx, lon_idx, variables)
                
                # Download the subset
                response = self.session.get(subset_url)
                response.raise_for_status()
                
                # Extract filename from URL and add subset info
                base_filename = url.split("/")[-1]
                filename = f"subset_{base_filename}"
                filepath = os.path.join(output_dir, filename)
                
                # Save the file
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                
                downloaded_files.append(filepath)
                print(f"Downloaded: {filename}")
                
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
        
        return downloaded_files 