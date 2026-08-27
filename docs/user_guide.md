# Kimodo AI Virtual Stage - User Testing Guide

Welcome to **Kimodo AI Virtual Stage**! This guide walks you through launching the interactive application locally, positioning 3D actors, generating AI motion, orchestrating performances on the master timeline, and saving/loading projects.

---

## 🚀 1. Launching the App

Run the application entrypoint from the repository root:

```bash
cd /Users/macpro/.gemini/antigravity/scratch/kimodo-virtual-stage
python3 app.py
```

Open your browser and navigate to:
👉 **`http://localhost:7860`**

---

## 🎬 2. Directing & Testing the Virtual Stage

### Step 1: Manage Actors
- In the left sidebar under **Actors**, you will see default actors: `Actor 01` and `Actor 02`.
- Click **+ Add** to spawn additional SOMA actors (`Actor 03`, `Actor 04`).
- Click on any actor (`Actor 01` or `Actor 02`) to select it.

### Step 2: Position & Rotate Actors
- Under **Transform**, use the **Position X** and **Position Z** sliders to position your selected actor on the 3D stage grid.
- Notice the 3D character mesh updates its position instantly in the 3D viewport canvas.

### Step 3: Direct AI Motion
- In the **Direct Motion** panel, type a natural language prompt, e.g.:
  > `"Walk forward slowly and wave with the right hand."`
- Click **Generate Motion**.
- The motion is generated via Kimodo and cached as a persistent `.npz` file in `storage/motions/`.

### Step 4: Master Timeline Synchronous Playback
- In the bottom **Master Timeline** panel:
  - Click **▶ Play All**.
  - Watch all actors execute their assigned performance simultaneously on the 3D stage grid.
  - Click **⏸ Pause** or **⏹ Stop** at any time.

### Step 5: Save & Load Project
- Click **Save Project** in the top navigation bar to write your master scene configuration to `storage/projects/`.
- Click **Load Project** to restore your exact scene arrangement and motion assignments anytime!
