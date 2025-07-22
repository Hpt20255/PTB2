import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { EquationData } from '../types';

interface Equation {
  id: number;
  a: number;
  b: number;
  c: number;
  equation_string: string;
  solution: string;
  solution_type: string;
  discriminant: number | null;
  created_at: string;
  updated_at: string;
}

interface EquationListProps {
  onEquationSelect?: (equation: EquationData) => void;
  onEquationUpdated?: (equation: EquationData) => void;
  onEquationDeleted?: (id: number) => void;
  onError?: (message: string) => void;
  refreshTrigger?: number; // Trigger to refresh the list
}

const EquationList: React.FC<EquationListProps> = ({
  onEquationSelect,
  onEquationUpdated,
  onEquationDeleted,
  onError,
  refreshTrigger = 0
}) => {
  const [equations, setEquations] = useState<Equation[]>([]);
  const [loading, setLoading] = useState(false);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [editForm, setEditForm] = useState({ a: 0, b: 0, c: 0 });
  const [currentPage, setCurrentPage] = useState(1);
  const [itemsPerPage] = useState(10);

  // Fetch all equations from API
  const fetchEquations = async () => {
    setLoading(true);
    try {
      const response = await axios.get('http://localhost:5000/api/equation');
      
      if (response.data.status === 'success') {
        setEquations(response.data.data || []);
      } else {
        onError?.('Failed to fetch equations: ' + response.data.message);
      }
    } catch (error: any) {
      console.error('Error fetching equations:', error);
      onError?.('Network error: ' + (error.message || 'Unable to fetch equations'));
    } finally {
      setLoading(false);
    }
  };

  // Load equations on component mount and when refreshTrigger changes
  useEffect(() => {
    fetchEquations();
  }, [refreshTrigger]);

  // Handle edit button click
  const handleEditClick = (equation: Equation) => {
    setEditingId(equation.id);
    setEditForm({
      a: equation.a,
      b: equation.b,
      c: equation.c
    });
  };

  // Handle edit form submission
  const handleEditSubmit = async (id: number) => {
    try {
      const response = await axios.put(`http://localhost:5000/api/equation/${id}`, editForm, {
        headers: { 'Content-Type': 'application/json' }
      });

      if (response.data.status === 'success') {
        const updatedEquation = response.data.data;
        
        // Update local state
        setEquations(prev => 
          prev.map(eq => eq.id === id ? updatedEquation : eq)
        );
        
        // Reset editing state
        setEditingId(null);
        setEditForm({ a: 0, b: 0, c: 0 });
        
        // Notify parent component - Convert to EquationData
        const equationData: EquationData = {
          id: updatedEquation.id,
          a: updatedEquation.a,
          b: updatedEquation.b,
          c: updatedEquation.c,
          solution: updatedEquation.solution,
          solution_type: updatedEquation.solution_type,
          discriminant: updatedEquation.discriminant || undefined
        };
        onEquationUpdated?.(equationData);
        
      } else {
        onError?.('Failed to update equation: ' + response.data.message);
      }
    } catch (error: any) {
      console.error('Error updating equation:', error);
      onError?.('Update failed: ' + (error.message || 'Network error'));
    }
  };

  // Handle delete button click
  const handleDelete = async (id: number, equationString: string) => {
    if (!window.confirm(`Bạn có chắc muốn xóa phương trình "${equationString}"?`)) {
      return;
    }

    try {
      const response = await axios.delete(`http://localhost:5000/api/equation/${id}`);

      if (response.data.status === 'success') {
        // Update local state
        setEquations(prev => prev.filter(eq => eq.id !== id));
        
        // Notify parent component
        onEquationDeleted?.(id);
        
      } else {
        onError?.('Failed to delete equation: ' + response.data.message);
      }
    } catch (error: any) {
      console.error('Error deleting equation:', error);
      onError?.('Delete failed: ' + (error.message || 'Network error'));
    }
  };

  // Handle equation row click
  const handleRowClick = (equation: Equation) => {
    if (editingId !== equation.id) {
      // Convert Equation to EquationData
      const equationData: EquationData = {
        id: equation.id,
        a: equation.a,
        b: equation.b,
        c: equation.c,
        solution: equation.solution,
        solution_type: equation.solution_type,
        discriminant: equation.discriminant || undefined
      };
      onEquationSelect?.(equationData);
    }
  };

  // Cancel editing
  const handleCancelEdit = () => {
    setEditingId(null);
    setEditForm({ a: 0, b: 0, c: 0 });
  };

  // Get solution type styling
  const getSolutionTypeStyle = (type: string) => {
    const styles = {
      two_real: { color: '#28a745', icon: '🎯' },
      one_real: { color: '#ffc107', icon: '🎪' },
      complex: { color: '#6f42c1', icon: '🌀' },
      linear: { color: '#17a2b8', icon: '📏' },
      none: { color: '#dc3545', icon: '❌' },
      infinite: { color: '#20c997', icon: '♾️' }
    };
    return styles[type as keyof typeof styles] || { color: '#6c757d', icon: '❓' };
  };

  // Pagination logic
  const totalPages = Math.ceil(equations.length / itemsPerPage);
  const startIndex = (currentPage - 1) * itemsPerPage;
  const endIndex = startIndex + itemsPerPage;
  const currentEquations = equations.slice(startIndex, endIndex);

  if (loading) {
    return (
      <div className="card">
        <div style={{ textAlign: 'center', padding: '40px' }}>
          <div className="loading"></div>
          <p style={{ marginTop: '15px', color: '#666' }}>Đang tải danh sách phương trình...</p>
        </div>
      </div>
    );
  }

  if (equations.length === 0) {
    return (
      <div className="card">
        <h3 style={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: '10px',
          color: '#495057'
        }}>
          📋 Danh sách phương trình đã lưu
        </h3>
        <div style={{ 
          textAlign: 'center', 
          padding: '40px',
          color: '#6c757d'
        }}>
          <p style={{ fontSize: '18px', marginBottom: '10px' }}>📝 Chưa có phương trình nào được lưu</p>
          <p style={{ fontSize: '14px' }}>Hãy tạo phương trình đầu tiên bằng form ở trên!</p>
        </div>
      </div>
    );
  }

  return (
    <div className="card equation-list-container">
      <h3 style={{ 
        display: 'flex', 
        alignItems: 'center', 
        gap: '10px',
        color: '#495057',
        marginBottom: '20px'
      }}>
        📋 Danh sách phương trình đã lưu ({equations.length})
      </h3>

      {/* Table */}
      <div className="equation-table-container">
        <table className="equation-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Phương trình</th>
              <th>Nghiệm</th>
              <th>Loại</th>
              <th>Δ</th>
              <th>Thời gian</th>
              <th>Thao tác</th>
            </tr>
          </thead>
          <tbody>
            {currentEquations.map((equation) => (
              <tr 
                key={equation.id}
                className={`equation-row ${editingId === equation.id ? 'editing' : ''}`}
                onClick={() => handleRowClick(equation)}
              >
                <td className="id-cell">{equation.id}</td>
                
                <td className="equation-cell">
                  {editingId === equation.id ? (
                    <div className="edit-form">
                      <div className="coefficient-inputs">
                        <input
                          type="number"
                          step="any"
                          value={editForm.a}
                          onChange={(e) => setEditForm(prev => ({ ...prev, a: parseFloat(e.target.value) || 0 }))}
                          placeholder="a"
                          className="coeff-input"
                        />
                        <input
                          type="number"
                          step="any"
                          value={editForm.b}
                          onChange={(e) => setEditForm(prev => ({ ...prev, b: parseFloat(e.target.value) || 0 }))}
                          placeholder="b"
                          className="coeff-input"
                        />
                        <input
                          type="number"
                          step="any"
                          value={editForm.c}
                          onChange={(e) => setEditForm(prev => ({ ...prev, c: parseFloat(e.target.value) || 0 }))}
                          placeholder="c"
                          className="coeff-input"
                        />
                      </div>
                    </div>
                  ) : (
                    <span className="equation-display">{equation.equation_string}</span>
                  )}
                </td>
                
                <td className="solution-cell">
                  <span className="solution-text">{equation.solution}</span>
                </td>
                
                <td className="type-cell">
                  <span 
                    className="solution-type-badge"
                    style={{ color: getSolutionTypeStyle(equation.solution_type).color }}
                  >
                    {getSolutionTypeStyle(equation.solution_type).icon} {equation.solution_type}
                  </span>
                </td>
                
                <td className="discriminant-cell">
                  {equation.discriminant !== null ? equation.discriminant.toFixed(2) : 'N/A'}
                </td>
                
                <td className="time-cell">
                  {new Date(equation.created_at).toLocaleString('vi-VN')}
                </td>
                
                <td className="actions-cell">
                  {editingId === equation.id ? (
                    <div className="edit-actions">
                      <button
                        className="btn btn-success btn-sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleEditSubmit(equation.id);
                        }}
                        title="Lưu thay đổi"
                      >
                        ✅
                      </button>
                      <button
                        className="btn btn-secondary btn-sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleCancelEdit();
                        }}
                        title="Hủy"
                      >
                        ❌
                      </button>
                    </div>
                  ) : (
                    <div className="row-actions">
                      <button
                        className="btn btn-primary btn-sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleEditClick(equation);
                        }}
                        title="Chỉnh sửa"
                      >
                        ✏️
                      </button>
                      <button
                        className="btn btn-danger btn-sm"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDelete(equation.id, equation.equation_string);
                        }}
                        title="Xóa"
                      >
                        🗑️
                      </button>
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="pagination-container">
          <div className="pagination-info">
            Hiển thị {startIndex + 1}-{Math.min(endIndex, equations.length)} của {equations.length} phương trình
          </div>
          <div className="pagination-controls">
            <button
              className="btn btn-outline-primary btn-sm"
              onClick={() => setCurrentPage(prev => Math.max(1, prev - 1))}
              disabled={currentPage === 1}
            >
              ← Trước
            </button>
            
            <span className="page-info">
              Trang {currentPage} / {totalPages}
            </span>
            
            <button
              className="btn btn-outline-primary btn-sm"
              onClick={() => setCurrentPage(prev => Math.min(totalPages, prev + 1))}
              disabled={currentPage === totalPages}
            >
              Sau →
            </button>
          </div>
        </div>
      )}

      {/* Instructions */}
      <div className="list-instructions">
        <p>💡 <strong>Hướng dẫn:</strong></p>
        <ul>
          <li>Click vào dòng để xem chi tiết phương trình</li>
          <li>Dùng nút ✏️ để chỉnh sửa hệ số a, b, c</li>
          <li>Dùng nút 🗑️ để xóa phương trình</li>
          <li>Phương trình mới nhất hiển thị ở đầu danh sách</li>
        </ul>
      </div>
    </div>
  );
};

export default EquationList;