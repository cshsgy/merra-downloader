# MERRA Data Downloader

A Python tool for downloading and processing MERRA (Modern-Era Retrospective analysis for Research and Applications) data from NASA's Goddard Earth Sciences Data and Information Services Center (GES DISC).

## Features

- Download MERRA data for specified time ranges
- Extract data for specific geographic regions (latitude-longitude boxes)
- Select specific variables of interest
- Support for multiple MERRA products with different temporal resolutions
- Automatic processing and saving of data in NetCDF format
- For a complete list of datasets available: https://goldsmr5.gesdisc.eosdis.nasa.gov/opendap/MERRA2/

## Installation

1. Clone this repository:
```bash
git clone https://github.com/yourusername/merra-downloader.git
cd merra-downloader
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file in the project root with your NASA Earthdata credentials:
```
MERRA_USERNAME=your_username
MERRA_PASSWORD=your_password
```

## Configuration

Create a `config.json` file with the following structure:

```json
{
    "time_range": {
        "start": "2020-01-01",
        "end": "2020-01-31"
    },
    "box": {
        "north": 90,
        "south": -90,
        "east": 180,
        "west": -180
    },
    "variables": ["O3", "CO", "NO2"],
    "product": "M2I3NPASM"
}
```

### Configuration Options

- `time_range`: Specify the start and end dates for data download
- `box`: Define the geographic region using latitude and longitude boundaries
- `variables`: List of variables to extract from the data
- `product`: MERRA product ID (see available products below)

## Available Products

To see a list of available products and their details, run:
```bash
python main.py --list-products
```

Currently supported products:
- M2I3NPASM: 3-hourly instantaneous assimilated state on pressure levels
- M2T1NXFLX: 1-hourly time-averaged single-level diagnostics
- M2T1NXAER: 1-hourly time-averaged aerosol diagnostics

## Usage

1. Basic usage with default configuration:
```bash
python main.py
```

2. Specify a custom configuration file:
```bash
python main.py --config custom_config.json
```

3. Specify custom output directories:
```bash
python main.py --output-dir my_data --processed-dir my_processed_data
```

## Output

The tool creates two directories:
- `data/`: Contains the downloaded raw MERRA files
- `processed/`: Contains the processed files with selected variables and geographic region

## Project Structure

- `config.py`: Configuration management
- `products.py`: MERRA product catalog and definitions
- `downloader.py`: Data download functionality
- `processor.py`: Data processing and extraction
- `main.py`: Main script and command-line interface

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
