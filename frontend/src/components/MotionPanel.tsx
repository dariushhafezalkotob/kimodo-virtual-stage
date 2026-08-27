import React, { useState } from 'react';
import { ActorData } from '../types/stage';

interface MotionPanelProps {
  selectedActor: ActorData | null;
  onGenerateMotion: (prompt: string, duration: number) => void;
  onAcceptMotion: (motionId: string) => void;
  isGenerating: boolean;
}

export const MotionPanel: React.FC<MotionPanelProps> = ({
  selectedActor,
  onGenerateMotion,
  onAcceptMotion,
  isGenerating,
}) => {
  const [prompt, setPrompt] = useState('');
  const [duration, setDuration] = useState(5.0);

  if (!selectedActor) {
    return (
      <div className="motion-panel empty">
        <p>Select an actor from the left sidebar to direct motion.</p>
      </div>
    );
  }

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (prompt.trim()) {
      onGenerateMotion(prompt, duration);
    }
  };

  return (
    <div className="motion-panel">
      <h3>Direct {selectedActor.name}</h3>
      <form onSubmit={handleSubmit} className="motion-form">
        <div className="form-group">
          <label>Motion Prompt</label>
          <textarea
            value={prompt}
            onChange={(e) => setPrompt(e.target.value)}
            placeholder="e.g. Walk slowly toward the center, stop, and look to the left."
            rows={3}
          />
        </div>
        <div className="form-row">
          <div className="form-group">
            <label>Duration (seconds)</label>
            <input
              type="number"
              step="0.5"
              min="1"
              max="15"
              value={duration}
              onChange={(e) => setDuration(parseFloat(e.target.value))}
            />
          </div>
          <button
            type="submit"
            className="btn btn-primary btn-generate"
            disabled={isGenerating || !prompt.trim()}
          >
            {isGenerating ? 'Generating Kimodo Motion...' : 'Generate Motion'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default MotionPanel;
