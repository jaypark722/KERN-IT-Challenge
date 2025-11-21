import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import api from '../../services/api';
import './Dashboard.css';

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();
  const [summary, setSummary] = useState(null);
  const [projects, setProjects] = useState([]);
  const [recentEntries, setRecentEntries] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      const [summaryRes, projectsRes, entriesRes] = await Promise.all([
        api.get('/api/entries/summary'),
        api.get('/api/projects?status=active&include_stats=true'),
        api.get('/api/entries')
      ]);

      setSummary(summaryRes.data);
      setProjects(projectsRes.data);
      setRecentEntries(entriesRes.data.slice(0, 5)); // Last 5 entries
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  if (loading) {
    return (
      <div className="dashboard-loading">
        <div className="spinner"></div>
      </div>
    );
  }

  return (
    <div className="dashboard">
      <nav className="dashboard-nav">
        <div className="nav-brand">Time Keeper</div>
        <div className="nav-links">
          <button className="nav-link active" onClick={() => navigate('/dashboard')}>
            Dashboard
          </button>
          <button className="nav-link" onClick={() => navigate('/time-entries')}>
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

      <div className="dashboard-content container">
        <h1 className="dashboard-title">Dashboard</h1>

        {/* Summary Cards */}
        <div className="summary-grid">
          <div className="summary-card">
            <div className="summary-label">Total Hours</div>
            <div className="summary-value">{summary?.total_hours || 0}h</div>
          </div>
          <div className="summary-card">
            <div className="summary-label">Billable Hours</div>
            <div className="summary-value">{summary?.billable_hours || 0}h</div>
          </div>
          <div className="summary-card">
            <div className="summary-label">Non-Billable Hours</div>
            <div className="summary-value">{summary?.non_billable_hours || 0}h</div>
          </div>
          <div className="summary-card">
            <div className="summary-label">Total Entries</div>
            <div className="summary-value">{summary?.total_entries || 0}</div>
          </div>
        </div>

        {/* Active Projects */}
        <div className="card">
          <div className="card-header">Active Projects</div>
          {projects.length === 0 ? (
            <p className="empty-state">No active projects found</p>
          ) : (
            <div className="projects-grid">
              {projects.map((project) => (
                <div key={project.id} className="project-card">
                  <div
                    className="project-color"
                    style={{ backgroundColor: project.color }}
                  ></div>
                  <div className="project-info">
                    <h3>{project.name}</h3>
                    <p className="project-description">{project.description || 'No description'}</p>
                    <div className="project-stats">
                      <span>{project.total_hours || 0}h logged</span>
                      <span>{project.entry_count || 0} entries</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Recent Time Entries */}
        <div className="card">
          <div className="card-header">Recent Time Entries</div>
          {recentEntries.length === 0 ? (
            <p className="empty-state">No time entries found</p>
          ) : (
            <div className="table-container">
              <table className="table">
                <thead>
                  <tr>
                    <th>Project</th>
                    <th>Start Time</th>
                    <th>Duration</th>
                    <th>Notes</th>
                  </tr>
                </thead>
                <tbody>
                  {recentEntries.map((entry) => (
                    <tr key={entry.id}>
                      <td>{entry.project_name}</td>
                      <td>{new Date(entry.start_time).toLocaleString('en-GB', { 
                        year: 'numeric', 
                        month: '2-digit', 
                        day: '2-digit', 
                        hour: '2-digit', 
                        minute: '2-digit',
                        hour12: false 
                      })}</td>
                      <td>{entry.duration_hours || 0}h</td>
                      <td>{entry.notes || '-'}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          <div className="card-footer">
            <button
              className="btn btn-primary"
              onClick={() => navigate('/time-entries')}
            >
              View All Entries
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
