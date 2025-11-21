import React, { useState, useEffect } from 'react';
import api from '../../services/api';
import './TimeEntryForm.css';

const TimeEntryForm = ({ entry, projects, onSubmit, onCancel }) => {
  const [formData, setFormData] = useState({
    project_id: '',
    start_time: '',
    end_time: '',
    notes: '',
    is_billable: true
  });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    if (entry) {
      setFormData({
        project_id: entry.project_id,
        start_time: entry.start_time ? new Date(entry.start_time).toISOString().slice(0, 16) : '',
        end_time: entry.end_time ? new Date(entry.end_time).toISOString().slice(0, 16) : '',
        notes: entry.notes || '',
        is_billable: entry.is_billable
      });
    } else {
      // Set default start time to now
      const now = new Date();
      setFormData(prev => ({
        ...prev,
        start_time: now.toISOString().slice(0, 16)
      }));
    }
  }, [entry]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setFormData({
      ...formData,
      [name]: type === 'checkbox' ? checked : value
    });
    setError('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const payload = {
        ...formData,
        project_id: parseInt(formData.project_id)
      };

      if (entry) {
        await api.put(`/api/entries/${entry.id}`, payload);
      } else {
        await api.post('/api/entries', payload);
      }

      onSubmit();
    } catch (err) {
      setError(err.response?.data?.message || 'Failed to save time entry');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="time-entry-form">
      <div className="form-header">
        <h2>{entry ? 'Edit Time Entry' : 'New Time Entry'}</h2>
      </div>

      {error && <div className="alert alert-error">{error}</div>}

      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label className="form-label">Project *</label>
          <select
            name="project_id"
            value={formData.project_id}
            onChange={handleChange}
            className="form-select"
            required
          >
            <option value="">Select a project</option>
            {projects
              .filter(p => p.status === 'active')
              .map((project) => (
                <option key={project.id} value={project.id}>
                  {project.name}
                </option>
              ))}
          </select>
        </div>

        <div className="form-row">
          <div className="form-group">
            <label className="form-label">Start Time *</label>
            <input
              type="datetime-local"
              name="start_time"
              value={formData.start_time}
              onChange={handleChange}
              className="form-input"
              required
            />
          </div>

          <div className="form-group">
            <label className="form-label">End Time</label>
            <input
              type="datetime-local"
              name="end_time"
              value={formData.end_time}
              onChange={handleChange}
              className="form-input"
            />
          </div>
        </div>

        <div className="form-group">
          <label className="form-label">Notes</label>
          <textarea
            name="notes"
            value={formData.notes}
            onChange={handleChange}
            className="form-textarea"
            placeholder="What did you work on?"
            rows="4"
          />
        </div>

        <div className="form-group checkbox-group">
          <label className="checkbox-label">
            <input
              type="checkbox"
              name="is_billable"
              checked={formData.is_billable}
              onChange={handleChange}
            />
            <span>Billable</span>
          </label>
        </div>

        <div className="form-actions">
          <button
            type="button"
            onClick={onCancel}
            className="btn btn-secondary"
            disabled={loading}
          >
            Cancel
          </button>
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Saving...' : entry ? 'Update' : 'Create'}
          </button>
        </div>
      </form>
    </div>
  );
};

export default TimeEntryForm;
