#!/usr/bin/env python3
"""
Kimodo AI Virtual Stage - Interactive Web Server Entrypoint

Serves the Virtual Stage application on http://localhost:7860 with:
- Multi-Actor Scene Manager
- Kimodo Motion Generator & Cache Adapter
- Interactive 3D Stage Viewport (Grid, Lighting, Actor Meshes)
- Directing Panel (Text Prompt, Duration, Generate, Accept)
- Master Timeline Transport (Play All, Pause, Stop, Seek)
- Project Persistence (Save / Load)
"""

import os
import sys
import json
import time
import logging
from typing import Any, Dict, List, Optional
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse

from backend.app.scenes.scene_manager import SceneManager
from backend.app.kimodo.adapter import KimodoMotionGenerator
from backend.app.projects.project import Project
from backend.app.projects.save import save_project
from backend.app.projects.load import load_project

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("VirtualStage")

# Initialize Master Managers
scene_mgr = SceneManager()
motion_generator = KimodoMotionGenerator()

# Pre-populate default stage with Actor 01 & Actor 02
actor1 = scene_mgr.actor_manager.create_actor("Actor 01", position=[-1.0, 0.0, 0.0])
actor2 = scene_mgr.actor_manager.create_actor("Actor 02", position=[1.0, 0.0, 0.0])

HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kimodo AI Virtual Stage</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/three@0.128.0/examples/js/controls/OrbitControls.js"></script>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; }
        body { background: #0f172a; color: #f8fafc; height: 100vh; overflow: hidden; display: flex; flex-direction: column; }
        header { background: #1e293b; padding: 12px 20px; display: flex; align-items: center; justify-content: space-between; border-bottom: 1px solid #334155; }
        .brand { display: flex; align-items: center; gap: 10px; font-weight: bold; font-size: 1.1rem; }
        .brand span { font-size: 1.4rem; }
        .main-layout { display: flex; flex: 1; position: relative; overflow: hidden; }
        .sidebar { width: 300px; background: #1e293b; border-right: 1px solid #334155; display: flex; flex-direction: column; p: 15px; padding: 15px; gap: 20px; z-index: 10; }
        .panel { background: #0f172a; border: 1px solid #334155; border-radius: 8px; padding: 15px; }
        .panel h3 { font-size: 0.9rem; text-transform: uppercase; color: #94a3b8; margin-bottom: 12px; }
        .actor-item { display: flex; align-items: center; justify-content: space-between; padding: 10px; background: #1e293b; border-radius: 6px; margin-bottom: 8px; cursor: pointer; border: 2px solid transparent; }
        .actor-item.active { border-color: #3b82f6; background: #1e3a8a; }
        .actor-item:hover { background: #334155; }
        .btn { padding: 8px 14px; border-radius: 6px; border: none; font-weight: 600; cursor: pointer; transition: all 0.2s; font-size: 0.85rem; }
        .btn-primary { background: #2563eb; color: white; }
        .btn-primary:hover { background: #1d4ed8; }
        .btn-secondary { background: #475569; color: white; }
        .btn-secondary:hover { background: #334155; }
        .btn-success { background: #16a34a; color: white; }
        .btn-success:hover { background: #15803d; }
        .viewport-container { flex: 1; position: relative; background: #020617; }
        #canvas3d { width: 100%; height: 100%; display: block; }
        .timeline-bar { height: 110px; background: #1e293b; border-top: 1px solid #334155; padding: 10px 20px; display: flex; flex-direction: column; gap: 10px; }
        .transport { display: flex; align-items: center; gap: 15px; }
        .time-display { font-family: monospace; color: #38bdf8; font-size: 1.1rem; }
        textarea, input[type="text"], input[type="number"] { width: 100%; background: #0f172a; border: 1px solid #334155; color: white; padding: 8px; border-radius: 6px; margin-top: 6px; }
        .slider-group { margin-top: 10px; }
        .slider-group label { font-size: 0.8rem; color: #94a3b8; }
        .slider-group input { width: 100%; }
        .track-lane { height: 24px; background: #0f172a; border-radius: 4px; position: relative; margin-top: 4px; }
        .clip { position: absolute; height: 100%; background: #3b82f6; border-radius: 4px; display: flex; align-items: center; padding: 0 8px; font-size: 0.75rem; font-weight: bold; }
    </style>
</head>
<body>
    <header>
        <div class="brand">
            <span>🏃</span> Kimodo AI Virtual Stage
        </div>
        <div style="display:flex; gap:10px;">
            <button class="btn btn-secondary" onclick="saveProject()">Save Project</button>
            <button class="btn btn-secondary" onclick="loadProject()">Load Project</button>
        </div>
    </header>

    <div class="main-layout">
        <div class="sidebar">
            <div class="panel">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                    <h3>Actors</h3>
                    <button class="btn btn-primary" style="padding:4px 8px;" onclick="addActor()">+ Add</button>
                </div>
                <div id="actors-list"></div>
            </div>

            <div class="panel">
                <h3>Transform (<span id="active-actor-name">None</span>)</h3>
                <div class="slider-group">
                    <label>Position X (<span id="pos-x-val">0</span>)</label>
                    <input type="range" id="pos-x" min="-5" max="5" step="0.1" value="0" oninput="updateTransform()">
                </div>
                <div class="slider-group">
                    <label>Position Z (<span id="pos-z-val">0</span>)</label>
                    <input type="range" id="pos-z" min="-5" max="5" step="0.1" value="0" oninput="updateTransform()">
                </div>
            </div>

            <div class="panel">
                <h3>Direct Motion</h3>
                <textarea id="prompt-input" rows="3" placeholder="e.g. Walk forward slowly and wave with the right hand."></textarea>
                <div style="margin-top:10px; display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:0.8rem; color:#94a3b8;">Duration: 5s</span>
                    <button class="btn btn-success" onclick="generateMotion()">Generate Motion</button>
                </div>
                <div id="status-msg" style="margin-top:8px; font-size:0.8rem; color:#38bdf8;"></div>
            </div>
        </div>

        <div class="viewport-container">
            <canvas id="canvas3d"></canvas>
        </div>
    </div>

    <div class="timeline-bar">
        <div class="transport">
            <button class="btn btn-primary" id="btn-play" onclick="togglePlay()">▶ Play All</button>
            <button class="btn btn-secondary" onclick="stopPlay()">⏹ Stop</button>
            <div class="time-display"><span id="clock-val">0.00</span>s / 15.00s</div>
        </div>
        <div id="timeline-tracks" style="display:flex; flex-direction:column; gap:4px;"></div>
    </div>

    <script>
        let sceneState = { actors: [], active_actor_id: null, is_playing: false, master_clock: 0 };
        let scene, camera, renderer, controls;
        let actorMeshes = {};

        function init3D() {
            const container = document.querySelector('.viewport-container');
            scene = new THREE.Scene();
            scene.background = new THREE.Color(0x020617);

            camera = new THREE.PerspectiveCamera(50, container.clientWidth / container.clientHeight, 0.1, 100);
            camera.position.set(0, 3, 7);

            renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('canvas3d'), antialias: true });
            renderer.setSize(container.clientWidth, container.clientHeight);

            controls = new THREE.OrbitControls(camera, renderer.domElement);
            controls.target.set(0, 1, 0);
            controls.update();

            const gridHelper = new THREE.GridHelper(20, 20, 0x3b82f6, 0x1e293b);
            scene.add(gridHelper);

            const light = new THREE.DirectionalLight(0xffffff, 1.2);
            light.position.set(5, 10, 7);
            scene.add(light);
            scene.add(new THREE.AmbientLight(0xffffff, 0.5));

            window.addEventListener('resize', () => {
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            });

            animate();
            fetchState();
        }

        function createDummyCharacterMesh(colorHex) {
            const group = new THREE.Group();
            const mat = new THREE.MeshStandardMaterial({ color: colorHex, roughness: 0.3 });

            // Torso
            const torso = new THREE.Mesh(new THREE.CylinderGeometry(0.2, 0.15, 0.7, 16), mat);
            torso.position.y = 1.0;
            group.add(torso);

            // Head
            const head = new THREE.Mesh(new THREE.SphereGeometry(0.12, 16, 16), mat);
            head.position.y = 1.5;
            group.add(head);

            return group;
        }

        function update3DScene() {
            sceneState.actors.forEach(actor => {
                if (!actorMeshes[actor.id]) {
                    const color = actor.id === 'actor_001' ? 0x3b82f6 : (actor.id === 'actor_002' ? 0x10b981 : 0xf59e0b);
                    const mesh = createDummyCharacterMesh(color);
                    scene.add(mesh);
                    actorMeshes[actor.id] = mesh;
                }
                const mesh = actorMeshes[actor.id];
                mesh.position.set(actor.position[0], actor.position[1], actor.position[2]);
                mesh.visible = actor.visible;

                // Animate waving if motion_id is set and playing
                if (sceneState.is_playing && actor.motion_id) {
                    mesh.rotation.y = Math.sin(sceneState.master_clock * 2) * 0.2;
                    mesh.position.x = actor.position[0] + Math.sin(sceneState.master_clock) * 0.5;
                }
            });
        }

        function animate() {
            requestAnimationFrame(animate);
            if (sceneState.is_playing) {
                sceneState.master_clock = (sceneState.master_clock + 0.03) % 15.0;
                document.getElementById('clock-val').innerText = sceneState.master_clock.toFixed(2);
                update3DScene();
            }
            renderer.render(scene, camera);
        }

        async function fetchState() {
            const res = await fetch('/api/state');
            sceneState = await res.json();
            renderUI();
            update3DScene();
        }

        function renderUI() {
            const listEl = document.getElementById('actors-list');
            listEl.innerHTML = '';
            sceneState.actors.forEach(actor => {
                const div = document.createElement('div');
                div.className = `actor-item ${actor.id === sceneState.active_actor_id ? 'active' : ''}`;
                div.onclick = () => selectActor(actor.id);
                div.innerHTML = `<span>👤 ${actor.name}</span><span style="font-size:0.75rem; color:#94a3b8;">${actor.motion_id ? '✓ Motion' : 'No Motion'}</span>`;
                listEl.appendChild(div);
            });

            const active = sceneState.actors.find(a => a.id === sceneState.active_actor_id);
            if (active) {
                document.getElementById('active-actor-name').innerText = active.name;
                document.getElementById('pos-x').value = active.position[0];
                document.getElementById('pos-z').value = active.position[2];
                document.getElementById('pos-x-val').innerText = active.position[0];
                document.getElementById('pos-z-val').innerText = active.position[2];
            }

            const tracksEl = document.getElementById('timeline-tracks');
            tracksEl.innerHTML = '';
            sceneState.actors.forEach(actor => {
                const track = document.createElement('div');
                track.style.cssText = 'display:flex; align-items:center; gap:10px; font-size:0.8rem;';
                track.innerHTML = `<span style="width:80px;">${actor.name}</span><div class="track-lane" style="flex:1;"><div class="clip" style="left:0; width:${actor.motion_id ? '40%' : '0%'};">${actor.motion_id || ''}</div></div>`;
                tracksEl.appendChild(track);
            });
        }

        async function selectActor(id) {
            await fetch(`/api/actor/select?id=${id}`);
            fetchState();
        }

        async function addActor() {
            await fetch('/api/actor/add');
            fetchState();
        }

        async function updateTransform() {
            const x = parseFloat(document.getElementById('pos-x').value);
            const z = parseFloat(document.getElementById('pos-z').value);
            document.getElementById('pos-x-val').innerText = x;
            document.getElementById('pos-z-val').innerText = z;
            await fetch(`/api/actor/transform?x=${x}&z=${z}`);
            fetchState();
        }

        async function generateMotion() {
            const prompt = document.getElementById('prompt-input').value;
            if (!prompt) return;
            document.getElementById('status-msg').innerText = "Generating motion...";
            const res = await fetch(`/api/motion/generate?prompt=${encodeURIComponent(prompt)}`);
            const data = await res.json();
            document.getElementById('status-msg').innerText = "Motion accepted & cached!";
            fetchState();
        }

        async function togglePlay() {
            sceneState.is_playing = !sceneState.is_playing;
            document.getElementById('btn-play').innerText = sceneState.is_playing ? "⏸ Pause" : "▶ Play All";
            await fetch(`/api/playback?play=${sceneState.is_playing}`);
        }

        async function stopPlay() {
            sceneState.is_playing = false;
            sceneState.master_clock = 0;
            document.getElementById('clock-val').innerText = "0.00";
            document.getElementById('btn-play').innerText = "▶ Play All";
            await fetch('/api/playback?play=false&reset=true');
            update3DScene();
        }

        async function saveProject() {
            await fetch('/api/project/save');
            alert("Project saved successfully to storage/projects/");
        }

        async function loadProject() {
            await fetch('/api/project/load');
            fetchState();
            alert("Project loaded!");
        }

        window.onload = init3D;
    </script>
</body>
</html>
"""

class RequestHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        params = urllib.parse.parse_qs(parsed.query)

        if parsed.path == "/" or parsed.path == "/index.html":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(HTML_TEMPLATE.encode("utf-8"))
            return

        if parsed.path == "/api/state":
            self.send_json(scene_mgr.get_scene_state())
            return

        if parsed.path == "/api/actor/add":
            new_actor = scene_mgr.actor_manager.create_actor()
            self.send_json(new_actor.to_dict())
            return

        if parsed.path == "/api/actor/select":
            actor_id = params.get("id", [None])[0]
            selected = scene_mgr.actor_manager.select_actor(actor_id)
            self.send_json(selected.to_dict() if selected else {})
            return

        if parsed.path == "/api/actor/transform":
            active = scene_mgr.actor_manager.get_active_actor()
            if active:
                x = float(params.get("x", [active.position[0]])[0])
                z = float(params.get("z", [active.position[2]])[0])
                scene_mgr.actor_manager.update_transform(active.id, position=[x, 0.0, z])
            self.send_json(scene_mgr.get_scene_state())
            return

        if parsed.path == "/api/motion/generate":
            prompt = params.get("prompt", ["Walk forward"])[0]
            active = scene_mgr.actor_manager.get_active_actor()
            if active:
                motion_res = motion_generator.generate(prompt=prompt, duration=5.0)
                motion_id = f"motion_{active.id}_001"
                motion_generator.cache_motion(motion_id, motion_res)
                scene_mgr.actor_manager.assign_motion(active.id, motion_id)
            self.send_json({"status": "success", "motion_id": motion_id})
            return

        if parsed.path == "/api/playback":
            play = params.get("play", ["false"])[0] == "true"
            reset = params.get("reset", ["false"])[0] == "true"
            if play:
                scene_mgr.play()
            else:
                scene_mgr.pause()
            if reset:
                scene_mgr.stop()
            self.send_json(scene_mgr.get_scene_state())
            return

        if parsed.path == "/api/project/save":
            proj = Project(
                name="Master Stage Scene",
                duration=scene_mgr.scene.duration,
                actors=scene_mgr.actor_manager.list_actors(),
            )
            filepath = save_project(proj)
            self.send_json({"status": "success", "filepath": filepath})
            return

        if parsed.path == "/api/project/load":
            proj = load_project("storage/projects/master_stage_scene.json")
            if proj:
                scene_mgr.actor_manager.actors.clear()
                for a_dict in proj.actors:
                    actor = scene_mgr.actor_manager.create_actor(
                        name=a_dict["name"],
                        position=a_dict.get("position"),
                        rotation=a_dict.get("rotation"),
                    )
                    actor.motion_id = a_dict.get("motion_id")
            self.send_json(scene_mgr.get_scene_state())
            return

        self.send_error(404, "Not Found")

    def send_json(self, data: Any):
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode("utf-8"))


def main():
    port = int(os.environ.get("PORT", 7860))
    server = HTTPServer(("0.0.0.0", port), RequestHandler)
    logger.info(f"============================================================")
    logger.info(f" Kimodo AI Virtual Stage Server running on http://localhost:{port}")
    logger.info(f"============================================================")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down server...")
        server.server_close()


if __name__ == "__main__":
    main()
