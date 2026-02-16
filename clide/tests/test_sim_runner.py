import unittest
import os
import shutil
import tempfile
from clide.sim_runner import SimulationWorkspace

class TestSimulationWorkspace(unittest.TestCase):
    def setUp(self):
        self.base_tmp = "/data/data/com.termux/files/home/.gemini/tmp/test_sims"
        if not os.path.exists(self.base_tmp):
            os.makedirs(self.base_tmp)

    def tearDown(self):
        if os.path.exists(self.base_tmp):
            shutil.rmtree(self.base_tmp)

    def test_workspace_creation_and_deletion(self):
        ws = SimulationWorkspace(workspace_id="test_sim_1", base_dir=self.base_tmp)
        path = ws.create()
        
        self.assertTrue(os.path.exists(path))
        self.assertTrue(path.endswith("test_sim_1"))
        
        ws.delete()
        self.assertFalse(os.path.exists(path))

    def test_workspace_scaffolding(self):
        ws = SimulationWorkspace(workspace_id="test_sim_2", base_dir=self.base_tmp)
        path = ws.create()
        ws.scaffold()
        
        # Check for minimal structure
        self.assertTrue(os.path.exists(os.path.join(path, "src")))
        self.assertTrue(os.path.exists(os.path.join(path, "docs")))
        self.assertTrue(os.path.exists(os.path.join(path, "README.md")))

if __name__ == "__main__":
    unittest.main()
