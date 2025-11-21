import React, { useState } from 'react';
import api from '../../services/api';
import './ProjectList.css';

const ProjectList = ({ projects, onUpdate }) => {
  const [showForm, setShowForm] = useState(false);
  const [editingProject, setEditingProject] = useState(null);
  const [formData, setFormData] = useState({
    name: '',
    description: '',
    status: 'active',
    color: '#3B82F6'
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleEdit = (project) => {
    setEditingProject(project);
    setFormData({
      name: project.name,
      description: project.description || '',
      status: project.status,
      color: project.color
    });
    setShowForm(true);
  };

  const handleCreate = () => {
    setEditingProject(null);
    setFormData({
      name: '',
      description: '',
      status: 'active',
      color: '#3B82F6'
    });
    setShowForm(true);
  };

  const handleDelete = async (projectId) => {
    if (window.confirm('Are you sure? This will delete all associated time entries.')) {
      try {
        await api.delete(`/api/projects/${projectId}`);
        onUpdate();
      } catch (err) {
        alert('Failed to delete project');
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      if (editingProject) {
        await api.put(`/api/projects/${editingProject.id}`, formData);
      } else {
        await api.post('/api/projects', formData);
      }
      setShowForm(false);
      onUpdate();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to save project');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="project-list">
      <div className="project-list-header">
        <h3>Projects</h3>
        <button onClick={handleCreate} className="btn btn-primary">
          + New Project
        </button>
      </div>

      {showForm && (
        <div className="project-form-card">
          <h4>{editingProject ? 'Edit Project' : 'New Project'}</h4>
          {error && <div className="alert alert-error">{error}</div>}
          
          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label className="form-label">Project Name *</label>
              <input
                type="text"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                className="form-input"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Description</label>
              <textarea
                value={formData.description}
                onChange={(e) => setFormData({ ...formData, description: e.target.value })}
                className="form-textarea"
                rows="3"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Status</label>
                <select
                  value={formData.status}
                  onChange={(e) => setFormData({ ...formData, status: e.target.value })}
                  className="form-select"
                >
                  <option value="active">Active</option>
                  <option value="completed">Completed</option>
                  <option value="archived">Archived</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Color</label>
                <input
                  type="color"
                  value={formData.color}
                  onChange={(e) => setFormData({ ...formData, color: e.target.value })}
                  className="form-input color-input"
                />
              </div>
            </div>

            <div className="form-actions">
              <button
                type="button"
                onClick={() => setShowForm(false)}
                className="btn btn-secondary"
                disabled={loading}
              >
                Cancel
              </button>
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Saving...' : 'Save'}
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="projects-grid">
        {projects.map((project) => (
          <div key={project.id} className="project-item">
            <div className="project-color-bar" style={{ backgroundColor: project.color }}></div>
            <div className="project-content">
              <div className="project-header-row">
                <h4>{project.name}</h4>
                <span className={`status-badge status-${project.status}`}>
                  {project.status}
                </span>
              </div>
              <p className="project-desc">{project.description || 'No description'}</p>
              <div className="project-actions">
                <button onClick={() => handleEdit(project)} className="btn-text">
                  Edit
                </button>
                <button onClick={() => handleDelete(project.id)} className="btn-text text-danger">
                  Delete
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>

      {projects.length === 0 && (
        <p className="empty-state">No projects found. Create one to get started!</p>
      )}
    </div>
  );
};

export default ProjectList;
