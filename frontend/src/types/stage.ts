export interface ActorData {
  id: string;
  name: string;
  visible: boolean;
  position: [number, number, number];
  rotation: [number, number, number];
  scale: number;
  selected: boolean;
  motion_id: string | null;
  timeline_start: number;
}

export interface MotionMetadata {
  motion_id: string;
  prompt: string;
  duration: number;
  fps: number;
  num_frames: number;
  constraints?: Record<string, any>;
}

export interface SceneState {
  id: string;
  name: string;
  duration: number;
  fps: number;
  loop: boolean;
  master_time: number;
  is_playing: boolean;
  active_actor_id: string | null;
  actors: ActorData[];
}
