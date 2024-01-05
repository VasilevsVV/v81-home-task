import csv
from pathlib import Path
import const as const
from ontology import Ontology
import auxiliary as aux

def main():
    path = Path("resources")
    path.mkdir(parents=True, exist_ok=True)
    ont = Ontology(const.PROJECT_ID)
    res_path = ont.dump_to_csv("project_ontology")
    print(f"Project ontology saved to {res_path}")
    
    aux.make_histogram()
    aux.make_grouped_histogram()
    
if __name__ == "__main__":
    main()