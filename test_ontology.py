from ontology import Ontology
import ontology
import const
import unittest
import os
import auxiliary as aux

class Test_ontology_test(unittest.TestCase):
    def test_import(self):
        path = "resources/test_res_path.json"
        ontology.import_project_labels_as_json(const.PROJECT_ID, path)
        self.assertTrue(os.path.exists(path))
        os.remove(path)
        
    def test_ontology_init(self):
        ont = Ontology(const.PROJECT_ID)
        self.assertEqual(ont.get_project_id(), const.PROJECT_ID)
        self.assertEqual(ont.get_project_name(), "Data_Engineer_home_Assignment")
        self.assertEquals(len(ont.get_labels()), 3)
        
    def test_ontology_output(self):
        ont = Ontology(const.PROJECT_ID)
        self.assertEqual(len(ont.data_features()), 74)
        self.assertEqual(ont.data_features()[0], {'project_id': const.PROJECT_ID,
                                                'img_id': 'clnhm7dxv01g7076ufwk6dj6q',
                                                'img_name': 'dalmatian1.jpg',
                                                'label_id': 'clnhmci430khh07yv113u0ggo',
                                                'label_kind': 'Default',
                                                'annotator_email': 'recruitmentdataeng@gmail.com',
                                                'feature_id': 'clnhmi3rx00042v6ovlkx9xd0',
                                                'feature_name': 'Dark_Spot',
                                                'feature_type': 'object',
                                                'feature_data': {'height': 25.0, 'left': 236.0, 'top': 222.0, 'width': 23.0},
                                                'feature_data_type': 'ImageBoundingBox',})
        print(ont.data_features()[-1])
        self.assertEqual(ont.data_features()[-1], {'project_id': const.PROJECT_ID,
                                                   'img_id': 'clnhm7dxv01gf076u9s0h491y',
                                                   'img_name': 'dalmatian3.jpg',
                                                   'label_id': 'clnt797dp00t1071f68l9avxt',
                                                   'label_kind': 'Default',
                                                   'annotator_email': 'josephl@oddity.com',
                                                   'feature_id': 'clnt7ifw2003g3b6o57i3oi39',
                                                   'feature_name': 'Free text comments',
                                                   'feature_type': 'classification',
                                                   'feature_data_type': 'String',
                                                   'feature_data': 'Adult'})
        
    def test_ontology_filtering(self):
        ont = Ontology(const.PROJECT_ID)
        
        res = ont.filter_features_by({"feature_type": "classification"})
        self.assertEqual(len(res), 12)
        self.assertEqual(aux.select_items(res[0], ["feature_type"]), {'feature_type': 'classification'})
        
    def test_ontology_filtering_multicolumn(self):
        ont = Ontology(const.PROJECT_ID)
        res = ont.filter_features_by({"img_name": "dalmatian2.jpg", 
                                      "feature_type": "object",
                                      "feature_name": "White_Area"})
        self.assertEqual(aux.select_items(res[0], ["img_name", "feature_type", "feature_name"]), 
                         {"img_name": "dalmatian2.jpg", 
                        "feature_type": "object",
                        "feature_name": "White_Area"})
        self.assertEqual(len(res), 5)
        
        res = ont.filter_features_by({"img_name": "dalmatian2.jpg", 
                                      "feature_type": "object",
                                      "feature_name": "Dark_Spot"})
        self.assertEqual(aux.select_items(res[0], ["img_name", "feature_type", "feature_name"]), 
                         {"img_name": "dalmatian2.jpg", 
                        "feature_type": "object",
                        "feature_name": "Dark_Spot"})
        self.assertEqual(len(res), 12)
        
        res = ont.filter_features_by({"img_name": "dalmatian2.jpg", 
                                      "feature_type": "object",
                                      "feature_name": "White_Area_Free_Hand"})
        self.assertEqual(aux.select_items(res[0], ["img_name", "feature_type", "feature_name"]), 
                         {"img_name": "dalmatian2.jpg", 
                        "feature_type": "object",
                        "feature_name": "White_Area_Free_Hand"})
        self.assertEqual(len(res), 4)
    
if __name__ == '__main__':
    unittest.main()
