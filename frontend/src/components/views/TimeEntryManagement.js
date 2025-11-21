import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../services/api';
import TimeEntryTable from '../timeEntries/TimeEntryTable';
import TimeEntryForm from '../timeEntries/TimeEntryForm';
import ProjectList from '../projects/ProjectList';
import './TimeEntryManagement.css';

const TimeEntryManagement = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [activeTab, setActiveTab] = useState('entries'); // entries, projects
  const [entries, setEntries] = useState([]);
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [editingEntry, setEditingEntry] = useState(null);
  const [filters, setFilters] = useState({
    project_id: '',
    start_date: '',
    end_date: '',
    is_billable: ''
  });

  useEffect(() => {
    fetchData();
  }, [filters]);

  const fetchData = async () => {
    try {
      setLoading(true);
      
      // Build query params, excluding empty values
      const params = {};
      if (filters.project_id) params.project_id = filters.project_id;
      if (filters.start_date) params.start_date = filters.start_date;
      if (filters.end_date) params.end_date = filters.end_date;
      if (filters.is_billable !== '') params.is_billable = filters.is_billable;
      
      const [entriesRes, projectsRes] = await Promise.all([
        api.get('/api/entries', { params }),
        api.get('/api/projects')
      ]);
      setEntries(entriesRes.data);
      setProjects(projectsRes.data);
    } catch (error) {
      console.error('Failed to fetch data:', error);
      alert('Failed to load data. Please check the console for details.');
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  const handleCreateEntry = () => {
    setEditingEntry(null);
    setShowForm(true);
  };

  const handleEditEntry = (entry) => {
    setEditingEntry(entry);
    setShowForm(true);
  };

  const handleDeleteEntry = async (entryId) => {
    if (window.confirm('Are you sure you want to delete this entry?')) {
      try {
        await api.delete(`/api/entries/${entryId}`);
        fetchData();
      } catch (error) {
        console.error('Failed to delete entry:', error);
        alert('Failed to delete entry');
      }
    }
  };

  const handleFormSubmit = async () => {
    setShowForm(false);
    setEditingEntry(null);
    await fetchData();
  };

  const handleFormCancel = () => {
    setShowForm(false);
    setEditingEntry(null);
  };

  return (
    <div className="time-entry-management">
      <nav className="dashboard-nav">
        <div className="nav-brand">Time Keeper</div>
        <div className="nav-links">
          <button className="nav-link" onClick={() => navigate('/dashboard')}>
            Dashboard
          </button>
          <button className="nav-link active" onClick={() => navigate('/time-entries')}>
            Time Entries
          </button>
        </div>
        <div className="nav-user">
          <span>Welcome, {user?.username}</span>
          <button className="btn btn-secondary" onClick={handleLogout}>
            Logout
          </button>
        </div>
      </nav>

      <div className="content container">
        <div className="page-header">
          <h1>Time Entry Management</h1>
          <button className="btn btn-primary" onClick={handleCreateEntry}>
            + New Time Entry
          </button>
        </div>

        <div className="tabs">
          <button
            className={`tab ${activeTab === 'entries' ? 'active' : ''}`}
            onClick={() => setActiveTab('entries')}
          >
            Time Entries
          </button>
          <button
            className={`tab ${activeTab === 'projects' ? 'active' : ''}`}
            onClick={() => setActiveTab('projects')}
          >
            Projects
          </button>
        </div>

        {showForm && (
          <div className="modal-overlay" onClick={handleFormCancel}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <TimeEntryForm
                entry={editingEntry}
                projects={projects}
                onSubmit={handleFormSubmit}
                onCancel={handleFormCancel}
              />
            </div>
          </div>
        )}

        {activeTab === 'entries' && (
          <div className="card">
            <TimeEntryTable
              entries={entries}
              projects={projects}
              filters={filters}
              onFilterChange={setFilters}
              onEdit={handleEditEntry}
              onDelete={handleDeleteEntry}
              loading={loading}
            />
          </div>
        )}

        {activeTab === 'projects' && (
          <div className="card">
            <ProjectList projects={projects} onUpdate={fetchData} />
          </div>
        )}
      </div>
    </div>
  );
};

export default TimeEntryManagement;
