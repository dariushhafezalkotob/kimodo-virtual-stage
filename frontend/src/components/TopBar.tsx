import React from 'react';

interface TopBarProps {
  sceneName: string;
  onNewProject: () => void;
  onSaveProject: () => void;
  onLoadProject: () => void;
}

export const TopBar: React.FC<TopBarProps> = ({
  sceneName,
  onNewProject,
  onSaveProject,
  onLoadProject,
}) => {
  return (
    <header className="top-bar">
      <div className="brand">
        <span className="brand-logo">🏃</span>
        <h1 className="brand-title">Kimodo AI Virtual Stage</h1>
        <span className="scene-name">{sceneName}</span>
      </div>
      <div className="actions">
        <button onClick={onNewProject} className="btn btn-secondary">New Project</button>
        <button onClick={onSaveProject} className="btn btn-primary">Save</button>
        <button onClick={onLoadProject} className="btn btn-secondary">Load</button>
      </div>
    </header>
  );
};

export default TopBar;
