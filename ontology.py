import labelbox
import const
import json
import csv
import os
import auxiliary as aux


def import_project_labels_as_json(project_id, res_path):
    client = labelbox.Client(api_key=const.LB_API_KEY)
    project = client.get_project(project_id)

    labels = project.export_v2(params={
        "data_row_details": True,
        "metadata_fields": True,
        "attachments": True,
        "project_details": True,
        "performance_details": True,
        "label_details": True,
        "interpolated_frames": True})

    labels.wait_till_done()

    fl = open(res_path, "w")
    json.dump(labels.result, fl)
    fl.close()

class Ontology:
    'Class represents project ontology'
    
    DATA_ROW_KEYS = ("img_id", "img_name", "project_id")
    DATA_LABEL_KEYS = ("label_id", "label_kind", "annotator_email", "age", "text_comment")
    DATA_FEATURE_KEYS = ("feature_id", "feature_name", "feature_kind", "feature_data")
    
    @staticmethod
    def data_row_all_keys():
        return Ontology.DATA_ROW_KEYS + Ontology.DATA_LABEL_KEYS + Ontology.DATA_FEATURE_KEYS
    
    def __init__(self, project_id) -> None:
        self.__local_json_storage_path = "resources/project_{}_ontology.json".format(project_id)
        self.__project_id = project_id
        self.__data_rows = None
        self.__data_labels = None
        self.__source_labels = self.__load_project_labels()
        self.__project_name = self.__find_project_name()
        
    def __load_project_labels(self):
        if (not os.path.exists(self.__local_json_storage_path)):
            import_project_labels_as_json(self.__project_id, self.__local_json_storage_path)
        with open(self.__local_json_storage_path, "r") as f:
            return json.load(f)      
    
    def __find_project_name(self):
        return self.__source_labels[0]["projects"][self.__project_id]["name"]
        
    def get_labels(self):
        return self.__source_labels

    def get_project_id(self):
        return self.__project_id
    
    def get_project_name(self):
        return self.__project_name

    def __mk_data_row(self, row):
        data = row["data_row"]
        project = row["projects"].get(self.__project_id)
        return {"img_id": data["id"],   ## Must have and ID!
                "img_name": data.get("external_id", "No name!!"),
                "author": aux.get_in(data, ["details", "created_by"], "No author!!"),
                "project_id": self.__project_id,
                "project_name": self.__project_name,
                "labels": project["labels"]}

    def data_rows(self):
        if (self.__data_rows):
            return self.__data_rows
        rows = []
        for row in self.__source_labels:
            image_row = self.__mk_data_row(row)
            rows.append(image_row)
        self.__data_rows = rows
        return rows

    def __mk_label(self, label):
        data = aux.get_in(label, ["annotations", "classifications"])
        age = aux.find_by(data, "name", "Puppy/Adult")
        text = aux.find_by(data, "name", "Free text comments")
        return {"label_id": label["id"],
                "label_kind": label["label_kind"],
                "annotator_email": aux.get_in(label, ["label_details", "created_by"], "No annotator!"),
                "age": aux.get_in(age, ["radio_answer", "name"], "Undefined"),
                "text_comment": aux.get_in(text, ["text_answer", "content"], ""),
                "objects": aux.get_in(label, ["annotations", "objects"])
                }

    def data_labels(self):
        if(self.__data_labels):
            return self.__data_labels
        res = []
        for row in self.data_rows():
            row_data = aux.select_keys(row, Ontology.DATA_ROW_KEYS)
            for lbl in row["labels"]:
                data_label = row_data | self.__mk_label(lbl)
                res.append(data_label)
        self.__data_labels = res
        return res
    
    @staticmethod
    def __feature_data(obj):
        match obj.get("annotation_kind", "classification"):
            case "ImageBoundingBox": return obj["bounding_box"]
            case "ImageSegmentationMask": return aux.get_in(obj, ["mask", "url"])
    
    def __mk_feature(self, obj):
        return {"feature_id":   obj["feature_id"],
                "feature_name": obj["name"],
                "feature_kind": obj["annotation_kind"],
                "feature_data": self.__feature_data(obj)}
    
    def data_features(self):
        res = []
        for lbl in self.data_labels():
            label_data = aux.select_keys(lbl, Ontology.DATA_ROW_KEYS + Ontology.DATA_LABEL_KEYS)
            for obj in lbl["objects"]:
                feature = label_data | self.__mk_feature(obj)
                res.append(feature)
        return res

    def dump_to_csv(self, filename):
        filepath = "resources/{}.csv".format(filename)
        with open(filepath, "w") as f:
            dict_writer = csv.DictWriter(f, Ontology.data_row_all_keys())
            dict_writer.writeheader()
            dict_writer.writerows(self.data_features())
        return filepath

