import unittest
from backend.app.actors.actor_manager import ActorManager
from backend.app.scenes.scene_manager import SceneManager


class TestActorManager(unittest.TestCase):
    def test_actor_creation_and_selection(self):
        manager = ActorManager()
        actor1 = manager.create_actor("Actor 01", position=[0.0, 0.0, 0.0])
        actor2 = manager.create_actor("Actor 02", position=[2.0, 0.0, 0.0])

        self.assertEqual(len(manager.actors), 2)
        self.assertTrue(actor1.selected)
        self.assertFalse(actor2.selected)
        self.assertEqual(manager.active_actor_id, "actor_001")

        # Switch selection
        manager.select_actor("actor_002")
        self.assertFalse(actor1.selected)
        self.assertTrue(actor2.selected)
        self.assertEqual(manager.active_actor_id, "actor_002")

    def test_actor_transform_and_motion_assignment(self):
        manager = ActorManager()
        actor = manager.create_actor("Actor 01")

        updated = manager.update_transform("actor_001", position=[1.5, 0.0, -2.0], scale=1.2)
        self.assertEqual(updated.position, [1.5, 0.0, -2.0])
        self.assertEqual(updated.scale, 1.2)

        manager.assign_motion("actor_001", motion_id="motion_walk_01", timeline_start=2.5)
        self.assertEqual(actor.motion_id, "motion_walk_01")
        self.assertEqual(actor.timeline_start, 2.5)

    def test_scene_manager_synchronization(self):
        scene_mgr = SceneManager()
        scene_mgr.actor_manager.create_actor("Actor 01")
        scene_mgr.actor_manager.create_actor("Actor 02")
        scene_mgr.actor_manager.create_actor("Actor 03")

        state = scene_mgr.get_scene_state()
        self.assertEqual(len(state["actors"]), 3)
        self.assertFalse(state["is_playing"])
        self.assertEqual(state["master_clock"], 0.0)

        scene_mgr.play()
        self.assertTrue(scene_mgr.is_playing)

        scene_mgr.seek(5.0)
        self.assertEqual(scene_mgr.master_clock, 5.0)

        scene_mgr.stop()
        self.assertFalse(scene_mgr.is_playing)
        self.assertEqual(scene_mgr.master_clock, 0.0)


if __name__ == "__main__":
    unittest.main()
