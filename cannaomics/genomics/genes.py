"""Gene catalog and annotation utilities."""

from dataclasses import dataclass

import pandas as pd


@dataclass
class GeneInfo:
    """Information about a specific gene."""

    gene_id: str
    gene_name: str
    gene_family: str
    chromosome: str | None = None
    start: int | None = None
    end: int | None = None
    strand: str | None = None
    known_function: str = ""
    known_products: list[str] = None
    source: str = ""
    confidence_level: str = "low"

    def __post_init__(self):
        if self.known_products is None:
            self.known_products = []


# Pre-defined known Cannabis genes based on literature (Booth et al., etc.)
TPS_GENE_FAMILIES = [
    GeneInfo(
        gene_id="CsTPS1",
        gene_name="CsTPS1",
        gene_family="TPS-b",
        known_function="Terpene Synthase",
        known_products=["beta_myrcene", "alpha_pinene"],
        source="Booth et al. 2017",
        confidence_level="high",
    ),
    GeneInfo(
        gene_id="CsTPS2",
        gene_name="CsTPS2",
        gene_family="TPS-b",
        known_function="Terpene Synthase",
        known_products=["beta_caryophyllene", "alpha_humulene"],
        source="Booth et al. 2017",
        confidence_level="high",
    ),
    GeneInfo(
        gene_id="CsTPS3",
        gene_name="CsTPS3",
        gene_family="TPS-b",
        known_function="Terpene Synthase",
        known_products=["limonene", "beta_pinene"],
        source="Booth et al. 2017",
        confidence_level="high",
    ),
    GeneInfo(
        gene_id="CsTPS4",
        gene_name="CsTPS4",
        gene_family="TPS-a",
        known_function="Terpene Synthase",
        known_products=["beta_caryophyllene"],
        source="Booth et al. 2019",
        confidence_level="high",
    ),
    GeneInfo(
        gene_id="CsTPS5",
        gene_name="CsTPS5",
        gene_family="TPS-a",
        known_function="Terpene Synthase",
        known_products=["alpha_humulene"],
        source="Booth et al. 2019",
        confidence_level="high",
    ),
    GeneInfo(
        gene_id="CsTPS14",
        gene_name="CsTPS14",
        gene_family="TPS-b",
        known_function="Terpene Synthase",
        known_products=["limonene"],
        source="Booth et al. 2020",
        confidence_level="medium",
    ),
    GeneInfo(
        gene_id="CsTPS18",
        gene_name="CsTPS18",
        gene_family="TPS-g",
        known_function="Terpene Synthase",
        known_products=["linalool"],
        source="Booth et al. 2020",
        confidence_level="medium",
    ),
    GeneInfo(
        gene_id="CsTPS19",
        gene_name="CsTPS19",
        gene_family="TPS-g",
        known_function="Terpene Synthase",
        known_products=["linalool"],
        source="Booth et al. 2020",
        confidence_level="medium",
    ),
    GeneInfo(
        gene_id="CsTPS30",
        gene_name="CsTPS30",
        gene_family="TPS-a",
        known_function="Terpene Synthase",
        known_products=["terpinolene"],
        source="Booth et al. 2020",
        confidence_level="medium",
    ),
    GeneInfo(
        gene_id="CsTPS38",
        gene_name="CsTPS38",
        gene_family="TPS-b",
        known_function="Terpene Synthase",
        known_products=["ocimene"],
        source="Booth et al. 2020",
        confidence_level="medium",
    ),
]

CANNABINOID_GENES = [
    GeneInfo(
        gene_id="THCAS",
        gene_name="THCAS",
        gene_family="Cannabinoid Synthase",
        known_function="THCA Synthase",
        known_products=["THCA", "THC"],
        source="Multiple",
        confidence_level="high",
    ),
    GeneInfo(
        gene_id="CBDAS",
        gene_name="CBDAS",
        gene_family="Cannabinoid Synthase",
        known_function="CBDA Synthase",
        known_products=["CBDA", "CBD"],
        source="Multiple",
        confidence_level="high",
    ),
    GeneInfo(
        gene_id="CBCAS",
        gene_name="CBCAS",
        gene_family="Cannabinoid Synthase",
        known_function="CBCA Synthase",
        known_products=["CBCA", "CBC"],
        source="Multiple",
        confidence_level="high",
    ),
    GeneInfo(
        gene_id="OAC",
        gene_name="OAC",
        gene_family="Polyketide Cyclase",
        known_function="Olivetolic Acid Cyclase",
        known_products=["Olivetolic Acid"],
        source="Multiple",
        confidence_level="high",
    ),
    GeneInfo(
        gene_id="PT",
        gene_name="PT",
        gene_family="Prenyltransferase",
        known_function="Geranyl-pyrophosphate--olivetolic acid geranyltransferase",
        known_products=["CBGA", "CBG"],
        source="Multiple",
        confidence_level="high",
    ),
]

PRECURSOR_PATHWAY_GENES = [
    GeneInfo(
        gene_id="DXS",
        gene_name="DXS",
        gene_family="MEP Pathway",
        known_function="1-deoxy-D-xylulose-5-phosphate synthase",
    ),
    GeneInfo(
        gene_id="DXR",
        gene_name="DXR",
        gene_family="MEP Pathway",
        known_function="1-deoxy-D-xylulose 5-phosphate reductoisomerase",
    ),
    GeneInfo(
        gene_id="HDR",
        gene_name="HDR",
        gene_family="MEP Pathway",
        known_function="4-hydroxy-3-methylbut-2-enyl diphosphate reductase",
    ),
    GeneInfo(
        gene_id="HMGR",
        gene_name="HMGR",
        gene_family="MEV Pathway",
        known_function="3-hydroxy-3-methylglutaryl-coenzyme A reductase",
    ),
    GeneInfo(
        gene_id="IDI",
        gene_name="IDI",
        gene_family="MEV/MEP Pathway",
        known_function="Isopentenyl-diphosphate delta-isomerase",
    ),
    GeneInfo(
        gene_id="GPPS",
        gene_name="GPPS",
        gene_family="Prenyltransferase",
        known_function="Geranyl diphosphate synthase",
    ),
    GeneInfo(
        gene_id="FPPS",
        gene_name="FPPS",
        gene_family="Prenyltransferase",
        known_function="Farnesyl diphosphate synthase",
    ),
]


class GeneCatalog:
    """Catalog managing all known genes of interest."""

    def __init__(self):
        self.genes = {}
        # Load all predefined genes
        for g in TPS_GENE_FAMILIES + CANNABINOID_GENES + PRECURSOR_PATHWAY_GENES:
            self.genes[g.gene_id] = g

    def get_gene(self, gene_id: str) -> GeneInfo | None:
        """Get a gene by ID."""
        return self.genes.get(gene_id)

    def search(self, query: str) -> list[GeneInfo]:
        """Search genes by ID, name, family, or product."""
        query = query.lower()
        results = []
        for g in self.genes.values():
            if (
                query in g.gene_id.lower()
                or query in g.gene_name.lower()
                or query in g.gene_family.lower()
                or any(query in p.lower() for p in g.known_products)
            ):
                results.append(g)
        return results

    def get_by_family(self, family: str) -> list[GeneInfo]:
        """Get all genes in a specific family or matching a family prefix."""
        family_lower = family.lower()
        return [
            g
            for g in self.genes.values()
            if g.gene_family.lower().startswith(family_lower)
        ]

    def get_all_target_genes(self) -> list[GeneInfo]:
        """Get all registered genes."""
        return list(self.genes.values())

    def to_dataframe(self) -> pd.DataFrame:
        """Convert the catalog to a pandas DataFrame."""
        return pd.DataFrame([vars(g) for g in self.genes.values()])


# Singleton instance for general use
catalog = GeneCatalog()
