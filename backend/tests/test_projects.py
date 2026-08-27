import os
import unittest
import tempfile
from backend.app.projects.project import Project
from backend.app.projects.save import save_project
from backend.app.projects.load import load_project


class TestProjects(unittest.TestCase):
    def test_save_and_load_project(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            proj = Project(
                name="Test Virtual Stage Scene",
                duration=12.0,
                actors=[{"id": "actor_001", "name": "Actor 01", "position": [0, 0, 0]}],
            )

            filepath = save_project(proj, storage_dir=tmp_dir)
            self.assertTrue(os.path.exists(filepath))

            loaded = load_project(filepath)
            self.assertIsNotNone(loaded)
            self.assertEqual(loaded.name, "Test Virtual Stage Scene")
            self.assertEqual(loaded.duration, 12.0)
            self.assertEqual(len(loaded.actors), 1)


if __name__ == "__main__":
    unittest.main()
