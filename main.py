import labelbox
import json
import csv
import const as const
import ontology
import auxiliary as aux

# lst = [("Name", "Val1", "Val2"), ("Josh", 10, 20), ("Sarah", 13, 20)]
# with open("resources/test.csv", "w") as f:
#     wrtr = csv.writer(f,)
#     wrtr.writerows(lst)

aux.make_histogram()    

ont = ontology.Ontology(const.PROJECT_ID)
# res = [row["name"] for row in ont.data_rows()]
res = list(filter(lambda row: row["img_name"] == "dalmatian1.jpg", ont.data_rows()))[0]
print(ont.data_features())
