import React from 'react';
import { ActorData } from '../types/stage';

interface MasterTimelineProps {
  actors: ActorData[];
  masterTime: number;
  duration: number;
  isPlaying: boolean;
  onPlay: () => void;
  onPause: () => void;
  onStop: () => void;
  onSeek: (timecode: number) => void;
}

export const MasterTimeline: React.FC<MasterTimelineProps> = ({
  actors,
  masterTime,
  duration,
  isPlaying,
  onPlay,
  onPause,
  onStop,
  onSeek,
}) => {
  return (
    <footer className="master-timeline">
      <div className="timeline-toolbar">
        <div className="transport-controls">
          {isPlaying ? (
            <button onClick={onPause} className="btn-transport">⏸️ Pause</button>
          ) : (
            <button onClick={onPlay} className="btn-transport play">▶️ Play All</button>
          )}
          <button onClick={onStop} className="btn-transport">⏹️ Stop</button>
        </div>
        <div className="timecode-display">
          <span>{masterTime.toFixed(2)}s</span> / <span>{duration.toFixed(2)}s</span>
        </div>
      </div>
      <div className="timeline-tracks">
        {actors.map((actor) => (
          <div key={actor.id} className="timeline-track">
            <span className="track-label">{actor.name}</span>
            <div className="track-lane">
              {actor.motion_id && (
                <div
                  className="motion-clip"
                  style={{
                    left: `${(actor.timeline_start / duration) * 100}%`,
                    width: `40%`,
                  }}
                >
                  {actor.motion_id}
                </div>
              )}
            </div>
          </div>
        ))}
      </div>
    </footer>
  );
};

export default MasterTimeline;
