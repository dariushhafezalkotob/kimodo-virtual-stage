import os
import unittest
import tempfile
from backend.app.kimodo.adapter import KimodoMotionGenerator
from backend.app.kimodo.motion_io import MotionCacheManager


class TestKimodoAdapter(unittest.TestCase):
    def test_motion_cache_manager(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            cache_mgr = MotionCacheManager(cache_dir=tmp_dir)

            motion_data = {
                "prompt": "A person walks forward and waves.",
                "duration": 3.33,
                "fps": 30,
            }

            saved_path = cache_mgr.save_motion("motion_test_001", motion_data)
            self.assertTrue(os.path.exists(saved_path))

            loaded_data = cache_mgr.load_motion("motion_test_001")
            self.assertIsNotNone(loaded_data)
            self.assertEqual(loaded_data["prompt"], "A person walks forward and waves.")
            self.assertEqual(loaded_data["duration"], 3.33)

    def test_kimodo_generator_adapter(self):
        with tempfile.TemporaryDirectory() as tmp_dir:
            generator = KimodoMotionGenerator(cache_dir=tmp_dir)

            res = generator.generate("Walk forward", duration=4.0)
            self.assertEqual(res["status"], "success")
            self.assertEqual(res["duration"], 4.0)

            path = generator.cache_motion("motion_walk_01", res)
            self.assertTrue(os.path.exists(path))


if __name__ == "__main__":
    unittest.main()
