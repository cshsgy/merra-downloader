from dataclasses import dataclass
from typing import List, Dict

@dataclass
class MERRAProduct:
    name: str
    description: str
    frequency: str
    variables: List[str]
    base_url: str

class MERRAProductCatalog:
    """Catalog of available MERRA products."""
    
    PRODUCTS = {
        "M2I3NPASM": MERRAProduct(
            name="M2I3NPASM",
            description="3-hourly instantaneous assimilated state on pressure levels",
            frequency="3-hour",
            variables=["O3", "CO", "NO2", "T", "U", "V", "H", "PS"],
            base_url="https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2I3NPASM.5.12.4/"
        ),
        "M2T1NXFLX": MERRAProduct(
            name="M2T1NXFLX",
            description="1-hourly time-averaged single-level diagnostics",
            frequency="1-hour",
            variables=["PRECTOT", "EVAP", "LWGNT", "SWGNT"],
            base_url="https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXFLX.5.12.4/"
        ),
        "M2T1NXAER": MERRAProduct(
            name="M2T1NXAER",
            description="1-hourly time-averaged aerosol diagnostics",
            frequency="1-hour",
            variables=["BCSMASS", "DUSMASS", "OCSMASS", "SO2SMASS"],
            base_url="https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXAER.5.12.4/"
        )
    }

    @classmethod
    def get_product(cls, product_id: str) -> MERRAProduct:
        """Get product information by ID."""
        if product_id not in cls.PRODUCTS:
            raise ValueError(f"Product {product_id} not found in catalog")
        return cls.PRODUCTS[product_id]

    @classmethod
    def list_products(cls) -> Dict[str, MERRAProduct]:
        """List all available products."""
        return cls.PRODUCTS

    @classmethod
    def get_variables(cls, product_id: str) -> List[str]:
        """Get available variables for a product."""
        product = cls.get_product(product_id)
        return product.variables 