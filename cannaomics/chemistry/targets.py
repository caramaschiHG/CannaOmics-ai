"""Target compound definitions for Cannabis sativa chemotype analysis.

Provides curated ``CompoundInfo`` records for the 9 major terpenes and
10 major cannabinoids studied in CannaOmics, along with look-up helpers.

Examples
--------
>>> from cannaomics.chemistry.targets import get_compound
>>> info = get_compound("beta_myrcene")
>>> info.display_name
'β-Myrcene'
"""
# Greek letters and the Δ symbol below are intentional scientific notation
# used purely in human-readable ``display_name`` fields. They are not used in
# string identifiers, so ambiguous-unicode warnings are silenced for this
# file.
# ruff: noqa: RUF001

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class CompoundInfo:
    """Immutable record describing a single target compound.

    Attributes
    ----------
    id : str
        Machine-readable canonical identifier (snake_case).
    name : str
        Short canonical name.
    display_name : str
        Human-friendly display label (may include Greek letters).
    compound_class : {'terpene', 'cannabinoid'}
        Chemical class.
    cas_number : str or None
        CAS Registry Number, if known.
    molecular_formula : str or None
        Molecular formula, if known.
    """

    id: str
    name: str
    display_name: str
    compound_class: Literal["terpene", "cannabinoid"]
    cas_number: str | None = None
    molecular_formula: str | None = None


# ---------------------------------------------------------------------------
# Terpene targets (9)
# ---------------------------------------------------------------------------

TERPENE_TARGETS: list[CompoundInfo] = [
    CompoundInfo(
        id="beta_myrcene",
        name="beta_myrcene",
        display_name="β-Myrcene",
        compound_class="terpene",
        cas_number="123-35-3",
        molecular_formula="C10H16",
    ),
    CompoundInfo(
        id="limonene",
        name="limonene",
        display_name="D-Limonene",
        compound_class="terpene",
        cas_number="5989-27-5",
        molecular_formula="C10H16",
    ),
    CompoundInfo(
        id="alpha_pinene",
        name="alpha_pinene",
        display_name="α-Pinene",
        compound_class="terpene",
        cas_number="80-56-8",
        molecular_formula="C10H16",
    ),
    CompoundInfo(
        id="beta_pinene",
        name="beta_pinene",
        display_name="β-Pinene",
        compound_class="terpene",
        cas_number="127-91-3",
        molecular_formula="C10H16",
    ),
    CompoundInfo(
        id="beta_caryophyllene",
        name="beta_caryophyllene",
        display_name="β-Caryophyllene",
        compound_class="terpene",
        cas_number="87-44-5",
        molecular_formula="C15H24",
    ),
    CompoundInfo(
        id="alpha_humulene",
        name="alpha_humulene",
        display_name="α-Humulene",
        compound_class="terpene",
        cas_number="6753-98-6",
        molecular_formula="C15H24",
    ),
    CompoundInfo(
        id="terpinolene",
        name="terpinolene",
        display_name="Terpinolene",
        compound_class="terpene",
        cas_number="586-62-9",
        molecular_formula="C10H16",
    ),
    CompoundInfo(
        id="ocimene",
        name="ocimene",
        display_name="β-Ocimene",
        compound_class="terpene",
        cas_number="13877-91-3",
        molecular_formula="C10H16",
    ),
    CompoundInfo(
        id="linalool",
        name="linalool",
        display_name="Linalool",
        compound_class="terpene",
        cas_number="78-70-6",
        molecular_formula="C10H18O",
    ),
]

# ---------------------------------------------------------------------------
# Cannabinoid targets (10)
# ---------------------------------------------------------------------------

CANNABINOID_TARGETS: list[CompoundInfo] = [
    CompoundInfo(
        id="THCA",
        name="THCA",
        display_name="Δ⁹-THCA",
        compound_class="cannabinoid",
        cas_number="23978-85-0",
        molecular_formula="C22H30O4",
    ),
    CompoundInfo(
        id="THC",
        name="THC",
        display_name="Δ⁹-THC",
        compound_class="cannabinoid",
        cas_number="1972-08-3",
        molecular_formula="C21H30O2",
    ),
    CompoundInfo(
        id="CBDA",
        name="CBDA",
        display_name="CBDA",
        compound_class="cannabinoid",
        cas_number="1244-58-2",
        molecular_formula="C22H30O4",
    ),
    CompoundInfo(
        id="CBD",
        name="CBD",
        display_name="CBD",
        compound_class="cannabinoid",
        cas_number="13956-29-1",
        molecular_formula="C21H30O2",
    ),
    CompoundInfo(
        id="CBCA",
        name="CBCA",
        display_name="CBCA",
        compound_class="cannabinoid",
        cas_number="20408-52-0",
        molecular_formula="C22H30O4",
    ),
    CompoundInfo(
        id="CBC",
        name="CBC",
        display_name="CBC",
        compound_class="cannabinoid",
        cas_number="20675-51-8",
        molecular_formula="C21H30O2",
    ),
    CompoundInfo(
        id="CBGA",
        name="CBGA",
        display_name="CBGA",
        compound_class="cannabinoid",
        cas_number="25555-57-1",
        molecular_formula="C22H32O4",
    ),
    CompoundInfo(
        id="CBG",
        name="CBG",
        display_name="CBG",
        compound_class="cannabinoid",
        cas_number="25654-31-3",
        molecular_formula="C21H32O2",
    ),
    CompoundInfo(
        id="THCV",
        name="THCV",
        display_name="THCV",
        compound_class="cannabinoid",
        cas_number="31262-37-0",
        molecular_formula="C19H26O2",
    ),
    CompoundInfo(
        id="CBDV",
        name="CBDV",
        display_name="CBDV",
        compound_class="cannabinoid",
        cas_number="24274-48-4",
        molecular_formula="C19H26O2",
    ),
]

# ---------------------------------------------------------------------------
# Combined registry (private)
# ---------------------------------------------------------------------------

_COMPOUND_REGISTRY: dict[str, CompoundInfo] = {
    c.id: c for c in TERPENE_TARGETS + CANNABINOID_TARGETS
}


# ---------------------------------------------------------------------------
# Public helpers
# ---------------------------------------------------------------------------


def get_compound(name: str) -> CompoundInfo:
    """Retrieve a compound record by canonical name.

    Parameters
    ----------
    name : str
        Canonical compound identifier (e.g. ``'beta_myrcene'``, ``'THC'``).

    Returns
    -------
    CompoundInfo
        The matching compound record.

    Raises
    ------
    KeyError
        If *name* does not match any registered compound.

    Examples
    --------
    >>> get_compound("linalool").cas_number
    '78-70-6'
    """
    try:
        return _COMPOUND_REGISTRY[name]
    except KeyError:
        available = ", ".join(sorted(_COMPOUND_REGISTRY.keys()))
        raise KeyError(f"Unknown compound '{name}'. Available: {available}") from None


def get_compounds_by_class(
    cls: Literal["terpene", "cannabinoid"],
) -> list[CompoundInfo]:
    """Return all compounds belonging to a chemical class.

    Parameters
    ----------
    cls : {'terpene', 'cannabinoid'}
        The chemical class to filter by.

    Returns
    -------
    list[CompoundInfo]
        Compounds matching the requested class.

    Examples
    --------
    >>> len(get_compounds_by_class("terpene"))
    9
    """
    return [c for c in _COMPOUND_REGISTRY.values() if c.compound_class == cls]
