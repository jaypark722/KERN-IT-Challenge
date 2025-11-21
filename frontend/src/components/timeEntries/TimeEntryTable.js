import React from 'react';
import './TimeEntryTable.css';

const TimeEntryTable = ({ entries, projects, filters, onFilterChange, onEdit, onDelete, loading }) => {
  const handleFilterChange = (e) => {
    const { name, value } = e.target;
    onFilterChange({ ...filters, [name]: value });
  };

  const clearFilters = () => {
    onFilterChange({
      project_id: '',
      start_date: '',
      end_date: '',
      is_billable: ''
    });
  };

  if (loading) {
    return <div className="spinner"></div>;
  }

  return (
    <div className="time-entry-table">
      <div className="filters">
        <div className="filter-group">
          <label>Project</label>
          <select
            name="project_id"
            value={filters.project_id}
            onChange={handleFilterChange}
            className="form-select"
          >
            <option value="">All Projects</option>
            {projects.map((project) => (
              <option key={project.id} value={project.id}>
                {project.name}
              </option>
            ))}
          </select>
        </div>

        <div className="filter-group">
          <label>Start Date</label>
          <input
            type="date"
            name="start_date"
            value={filters.start_date}
            onChange={handleFilterChange}
            className="form-input"
          />
        </div>

        <div className="filter-group">
          <label>End Date</label>
          <input
            type="date"
            name="end_date"
            value={filters.end_date}
            onChange={handleFilterChange}
            className="form-input"
          />
        </div>

        <div className="filter-group">
          <label>Billable</label>
          <select
            name="is_billable"
            value={filters.is_billable}
            onChange={handleFilterChange}
            className="form-select"
          >
            <option value="">All</option>
            <option value="true">Billable</option>
            <option value="false">Non-Billable</option>
          </select>
        </div>

        <div className="filter-group">
          <label>&nbsp;</label>
          <button onClick={clearFilters} className="btn btn-secondary">
            Clear Filters
          </button>
        </div>
      </div>

      {entries.length === 0 ? (
        <p className="empty-state">No time entries found</p>
      ) : (
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Project</th>
                <th>Start Time</th>
                <th>End Time</th>
                <th>Duration</th>
                <th>Billable</th>
                <th>Notes</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {entries.map((entry) => (
                <tr key={entry.id}>
                  <td>
                    <span className="project-badge">{entry.project_name}</span>
                  </td>
                  <td>{new Date(entry.start_time).toLocaleString('en-GB', { 
                    year: 'numeric', 
                    month: '2-digit', 
                    day: '2-digit', 
                    hour: '2-digit', 
                    minute: '2-digit',
                    hour12: false 
                  })}</td>
                  <td>
                    {entry.end_time ? new Date(entry.end_time).toLocaleString('en-GB', { 
                      year: 'numeric', 
                      month: '2-digit', 
                      day: '2-digit', 
                      hour: '2-digit', 
                      minute: '2-digit',
                      hour12: false 
                    }) : '-'}
                  </td>
                  <td>
                    <strong>{entry.duration_hours || 0}h</strong>
                  </td>
                  <td>
                    {entry.is_billable ? (
                      <span className="badge badge-success">Yes</span>
                    ) : (
                      <span className="badge badge-secondary">No</span>
                    )}
                  </td>
                  <td className="notes-cell">{entry.notes || '-'}</td>
                  <td>
                    <div className="action-buttons">
                      <button
                        onClick={() => onEdit(entry)}
                        className="btn-icon btn-edit"
                        title="Edit"
                      >
                        ✎
                      </button>
                      <button
                        onClick={() => onDelete(entry.id)}
                        className="btn-icon btn-delete"
                        title="Delete"
                      >
                        🗑
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}

      <div className="table-footer">
        <strong>Total Entries: {entries.length}</strong>
        <strong>
          Total Hours:{' '}
          {entries
            .reduce((sum, entry) => sum + (entry.duration_hours || 0), 0)
            .toFixed(2)}
          h
        </strong>
      </div>
    </div>
  );
};

export default TimeEntryTable;
