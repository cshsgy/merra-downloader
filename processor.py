import netCDF4 as nc
import numpy as np
from typing import List, Dict, Any
import os
from config import Config

class MERRAProcessor:
    def __init__(self, config: Config):
        self.config = config

    def _get_lat_lon_indices(self, dataset: nc.Dataset) -> tuple:
        """Get indices for the specified latitude-longitude box."""
        box = self.config.config["box"]
        lat = dataset.variables['lat'][:]
        lon = dataset.variables['lon'][:]
        
        lat_idx = np.where((lat >= box["south"]) & (lat <= box["north"]))[0]
        lon_idx = np.where((lon >= box["west"]) & (lon <= box["east"]))[0]
        
        return lat_idx, lon_idx

    def process_file(self, input_file: str, output_dir: str = "processed") -> str:
        """Process a single MERRA file and extract specified variables and region."""
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Open the input file
        with nc.Dataset(input_file, 'r') as ds:
            # Get indices for the specified box
            lat_idx, lon_idx = self._get_lat_lon_indices(ds)
            
            # Create output file
            output_filename = os.path.join(output_dir, f"processed_{os.path.basename(input_file)}")
            with nc.Dataset(output_filename, 'w') as out_ds:
                # Copy dimensions
                for dim_name, dim in ds.dimensions.items():
                    if dim_name == 'lat':
                        out_ds.createDimension(dim_name, len(lat_idx))
                    elif dim_name == 'lon':
                        out_ds.createDimension(dim_name, len(lon_idx))
                    else:
                        out_ds.createDimension(dim_name, len(dim))
                
                # Copy global attributes
                for attr_name, attr_value in ds.__dict__.items():
                    setattr(out_ds, attr_name, attr_value)
                
                # Process each requested variable
                for var_name in self.config.config["variables"]:
                    if var_name in ds.variables:
                        var = ds.variables[var_name]
                        
                        # Create variable in output file
                        out_var = out_ds.createVariable(
                            var_name,
                            var.dtype,
                            var.dimensions
                        )
                        
                        # Copy variable attributes
                        for attr_name, attr_value in var.__dict__.items():
                            setattr(out_var, attr_name, attr_value)
                        
                        # Extract data for the specified region
                        if 'lat' in var.dimensions and 'lon' in var.dimensions:
                            data = var[:, lat_idx, lon_idx]
                        else:
                            data = var[:]
                        
                        out_var[:] = data
        
        return output_filename

    def process_files(self, input_files: List[str], output_dir: str = "processed") -> List[str]:
        """Process multiple MERRA files."""
        processed_files = []
        for input_file in input_files:
            try:
                output_file = self.process_file(input_file, output_dir)
                processed_files.append(output_file)
                print(f"Processed: {os.path.basename(output_file)}")
            except Exception as e:
                print(f"Error processing {input_file}: {str(e)}")
        
        return processed_files 