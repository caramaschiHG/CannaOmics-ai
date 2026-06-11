"""Tests for genomics module."""

from cannaomics.genomics.genes import catalog


def test_gene_catalog_retrieval():
    gene = catalog.get_gene("THCAS")
    assert gene is not None
    assert "THC" in gene.known_products


def test_gene_search():
    results = catalog.search("limonene")
    assert len(results) > 0
    assert any("limonene" in g.known_products for g in results)


def test_get_by_family():
    tps_b = catalog.get_by_family("TPS-b")
    assert len(tps_b) > 0
    assert all(g.gene_family == "TPS-b" for g in tps_b)
