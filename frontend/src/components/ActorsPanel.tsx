import React from 'react';
import { ActorData } from '../types/stage';

interface ActorsPanelProps {
  actors: ActorData[];
  selectedActorId: string | null;
  onSelectActor: (actorId: string) => void;
  onAddActor: () => void;
  onToggleVisibility: (actorId: string) => void;
  onDeleteActor: (actorId: string) => void;
}

export const ActorsPanel: React.FC<ActorsPanelProps> = ({
  actors,
  selectedActorId,
  onSelectActor,
  onAddActor,
  onToggleVisibility,
  onDeleteActor,
}) => {
  return (
    <aside className="actors-panel">
      <div className="panel-header">
        <h2>Actors</h2>
        <button onClick={onAddActor} className="btn btn-sm btn-primary">+ Add Actor</button>
      </div>
      <ul className="actors-list">
        {actors.map((actor) => (
          <li
            key={actor.id}
            className={`actor-item ${actor.id === selectedActorId ? 'selected' : ''}`}
            onClick={() => onSelectActor(actor.id)}
          >
            <span className="actor-icon">👤</span>
            <span className="actor-name">{actor.name}</span>
            <div className="actor-controls" onClick={(e) => e.stopPropagation()}>
              <button
                className="btn-icon"
                onClick={() => onToggleVisibility(actor.id)}
                title={actor.visible ? "Hide Actor" : "Show Actor"}
              >
                {actor.visible ? "👁️" : "🙈"}
              </button>
              <button
                className="btn-icon danger"
                onClick={() => onDeleteActor(actor.id)}
                title="Delete Actor"
              >
                🗑️
              </button>
            </div>
          </li>
        ))}
      </ul>
    </aside>
  );
};

export default ActorsPanel;
