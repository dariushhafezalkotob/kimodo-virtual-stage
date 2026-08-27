# Kimodo AI Virtual Stage - System Architecture

## Architecture Overview

```text
                       USER INTERFACE
                ┌───────────────────────────┐
                │   React / Three.js / UI   │
                └─────────────┬─────────────┘
                              │ WebSocket / REST
                              ▼
                   BACKEND SCENE MANAGER
                ┌───────────────────────────┐
                │       SceneManager        │
                │  ActorManager / Timeline  │
                └─────────────┬─────────────┘
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
        MOTION CACHE                  KIMODO ADAPTER
      (storage/motions)             (KimodoMotionGenerator)
       .npz Array Load                      │
    0 GPU Inference Cost                    ▼
                                      NVIDIA KIMODO
                                      (Port 9550 / GPU)
```

## System Components

### 1. Kimodo Adapter (`backend/app/kimodo/`)
- `MotionGenerator`: Abstract interface ensuring backend pluggability.
- `KimodoMotionGenerator`: Interfaces with Kimodo text encoder on `:9550` and SOMA motion model.
- `MotionCacheManager`: Saves/loads `.npz` binary motion files and `.json` metadata to `storage/motions/`.

### 2. Multi-Actor Scene System (`backend/app/actors/`, `backend/app/scenes/`)
- `Actor`: Dataclass holding 3D position, rotation, visibility, assigned motion ID, and master timeline start offset.
- `ActorManager`: CRUD, active selection context, transform mutations, and duplication.
- `SceneManager`: Master playback clock, play/pause/stop/seek operations, and multi-actor synchronization.

### 3. Master Timeline & Playback (`backend/app/timeline/`)
- Synchronizes playback across all active actors from one master clock.
- Evaluates per-actor frame indices deterministically.

### 4. Virtual Stage Frontend (`frontend/src/`)
- `TopBar`: Project management controls.
- `ActorsPanel`: Multi-actor list, selection highlights, and visibility controls.
- `MotionPanel`: Text-to-motion direct panel with duration and prompt controls.
- `MasterTimeline`: Synchronous multi-actor timeline track view and master transport controls.
