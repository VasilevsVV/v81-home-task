from ontology import Ontology
import ontology
import const
import unittest
import os

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
    
if __name__ == '__main__':
    unittest.main()
