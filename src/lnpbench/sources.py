"""Metadata-only public source registry; no third-party records are redistributed."""

SOURCES = {
    "lipobart": {
        "title": "Representations of lipid nanoparticles using large language models",
        "url": "https://github.com/Sanofi-Public/LipoBART",
        "data_scope": "ionizable lipid SMILES and transfection labels",
        "license_note": "academic research and non-commercial use; verify upstream LICENSE.md",
    },
    "lnpdb": {
        "title": "Lipid Nanoparticle Database (LNPDB)",
        "url": "https://lnpdb.molcube.com/",
        "data_scope": "composition, experiment, performance and simulation metadata",
        "license_note": "verify database terms and per-study provenance before reuse",
    },
    "rna_size_gradient": {
        "title": "Benchmark formulations for encapsulation of RNA cargo size gradient",
        "url": "https://doi.org/10.1038/s41598-024-52685-1",
        "data_scope": "10–1929 nt payload sizes across benchmark LNP formulations",
        "license_note": "open-access article; use source tables under stated article license",
    },
}
