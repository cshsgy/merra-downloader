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
        # Instantaneous 3-hourly products
        "M2I3NPASM": MERRAProduct(
            name="M2I3NPASM",
            description="3-hourly instantaneous assimilated state on pressure levels",
            frequency="3-hour",
            variables=["O3", "CO", "NO2", "T", "U", "V", "H", "PS", "QV", "QL", "QI", "RH"],
            base_url="https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2I3NPASM.5.12.4/"
        ),
        "M2I3NVAER": MERRAProduct(
            name="M2I3NVAER",
            description="3-hourly instantaneous aerosol diagnostics on pressure levels",
            frequency="3-hour",
            variables=["BCSMASS", "DUSMASS", "OCSMASS", "SO2SMASS", "SSSMASS", "SO4SMASS"],
            base_url="https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2I3NVAER.5.12.4/"
        ),
        
        # Time-averaged 1-hourly products
        "M2T1NXFLX": MERRAProduct(
            name="M2T1NXFLX",
            description="1-hourly time-averaged single-level diagnostics",
            frequency="1-hour",
            variables=["PRECTOT", "EVAP", "LWGNT", "SWGNT", "PRECSNO", "SNOMAS", "TS", "T2M", "U10M", "V10M"],
            base_url="https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXFLX.5.12.4/"
        ),
        "M2T1NXAER": MERRAProduct(
            name="M2T1NXAER",
            description="1-hourly time-averaged aerosol diagnostics",
            frequency="1-hour",
            variables=["BCSMASS", "DUSMASS", "OCSMASS", "SO2SMASS", "SSSMASS", "SO4SMASS", "DUEXTTAU", "SSEXTTAU", "BCEXTTAU", "OCEXTTAU"],
            base_url="https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXAER.5.12.4/"
        ),
        "M2T1NXRAD": MERRAProduct(
            name="M2T1NXRAD",
            description="1-hourly time-averaged radiation diagnostics",
            frequency="1-hour",
            variables=["SWGDN", "SWGNT", "LWGNT", "ALBEDO", "CLDTOT", "CLDHGH", "CLDMED", "CLDLOW"],
            base_url="https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXRAD.5.12.4/"
        ),
        
        # Monthly mean products
        "M2TMNXAER": MERRAProduct(
            name="M2TMNXAER",
            description="Monthly mean aerosol diagnostics",
            frequency="monthly",
            variables=["BCSMASS", "DUSMASS", "OCSMASS", "SO2SMASS", "SSSMASS", "SO4SMASS", "DUEXTTAU", "SSEXTTAU", "BCEXTTAU", "OCEXTTAU"],
            base_url="https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2TMNXAER.5.12.4/"
        ),
        "M2TMNXFLX": MERRAProduct(
            name="M2TMNXFLX",
            description="Monthly mean single-level diagnostics",
            frequency="monthly",
            variables=["PRECTOT", "EVAP", "LWGNT", "SWGNT", "PRECSNO", "SNOMAS", "TS", "T2M", "U10M", "V10M"],
            base_url="https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2TMNXFLX.5.12.4/"
        ),
        "M2TMNXRAD": MERRAProduct(
            name="M2TMNXRAD",
            description="Monthly mean radiation diagnostics",
            frequency="monthly",
            variables=["SWGDN", "SWGNT", "LWGNT", "ALBEDO", "CLDTOT", "CLDHGH", "CLDMED", "CLDLOW"],
            base_url="https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2TMNXRAD.5.12.4/"
        ),
        
        # Land surface products
        "M2T1NXLND": MERRAProduct(
            name="M2T1NXLND",
            description="1-hourly time-averaged land surface diagnostics",
            frequency="1-hour",
            variables=["LAI", "GVEG", "RZMC", "SMC", "TSOIL1", "TSOIL2", "TSOIL3", "TSOIL4"],
            base_url="https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2T1NXLND.5.12.4/"
        ),
        "M2TMNXLND": MERRAProduct(
            name="M2TMNXLND",
            description="Monthly mean land surface diagnostics",
            frequency="monthly",
            variables=["LAI", "GVEG", "RZMC", "SMC", "TSOIL1", "TSOIL2", "TSOIL3", "TSOIL4"],
            base_url="https://goldsmr4.gesdisc.eosdis.nasa.gov/opendap/MERRA2/M2TMNXLND.5.12.4/"
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