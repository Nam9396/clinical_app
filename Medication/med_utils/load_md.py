from pathlib import Path
import streamlit as st

MED_REGISTRY = {

    # thuốc kháng sinh
    "Acyclovir": "antibiotic/acyclovir.md",
    "Amikacin": "antibiotic/amikacin.md",
    "Cefepime": "antibiotic/cefepime.md",
    "Cefotaxime": "antibiotic/cefotaxime.md",
    "Ceftazidime": "antibiotic/ceftazidime.md",
    "Ceftriaxone": "antibiotic/ceftriaxone.md",
    "Ciprofloxacin": "antibiotic/ciprofloxacin.md",
    "Clindamycin": "antibiotic/clindamycin.md",
    "Gentamicin": "antibiotic/gentamicin.md",
    "Imipenem": "antibiotic/imipenem.md",
    "Linezolid": "antibiotic/linezolid.md",
    "Meropenem": "antibiotic/meropenem.md",
    "Metronidazole": "antibiotic/metronidazole.md",
    "Oxacillin": "antibiotic/oxacillin.md",
    "Ticarcillin": "antibiotic/ticarcillin.md",
    "Vancomycin": "antibiotic/vancomycin.md", 

    # thuốc thần kinh
    "Diazepam": "neuromed/diazepam.md",
    "Fentanyl": "fentanyl.md",
    "Levetiracetam": "Levetiracetam.md",
    "Midazolam": "neuromed/midazolam.md",
    "Morphin": "morphin.md",
    "Phenobarbital": "neuromed/phenobarbital.md",
    "Promethazine": "promethazine.md"
}


@st.cache_data(show_spinner=False)
def load_med_markdown(med_code):
    protocol_uri = Path("Medication") / f"{MED_REGISTRY[med_code]}"
    return protocol_uri.read_text(encoding="utf-8") 
