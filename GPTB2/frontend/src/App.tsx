import React, { useState, useEffect } from 'react';
import EquationForm from './components/EquationForm';
import EquationResult from './components/EquationResult';
import { EquationData } from './types';
import { equationApi } from './services/api';

const App: React.FC = () => {
  const [apiStatus, setApiStatus] = useState<'checking' | 'connected' | 'error'>('checking');
  const [createdEquations, setCreatedEquations] = useState<EquationData[]>([]);
  const [currentEquation, setCurrentEquation] = useState<EquationData | null>(null);
  const [showSteps, setShowSteps] = useState<boolean>(false);
  const [notification, setNotification] = useState<{
    type: 'success' | 'error' | 'info';
    message: string;
  } | null>(null);

  // Check API connection on component mount
  useEffect(() => {
    checkApiConnection();
  }, []);

  const checkApiConnection = async () => {
    try {
      await equationApi.ping();
      setApiStatus('connected');
      console.log('✅ API connection successful');
    } catch (error) {
      setApiStatus('error');
      console.error('❌ API connection failed:', error);
    }
  };

  // Handle equation creation
  const handleEquationCreated = (equation: EquationData) => {
    setCreatedEquations(prev => [equation, ...prev]);
    setCurrentEquation(equation);
    setShowSteps(false); // Reset steps view
    
    // Show success notification
    setNotification({
      type: 'success',
      message: `✅ Phương trình đã được tạo thành công! ID: ${equation.id}`
    });
    
    // Clear notification after 5 seconds
    setTimeout(() => setNotification(null), 5000);
  };

  // Handle errors
  const handleError = (error: string) => {
    setNotification({
      type: 'error',
      message: `❌ ${error}`
    });
    
    // Clear notification after 8 seconds
    setTimeout(() => setNotification(null), 8000);
  };

  // Clear notification
  const clearNotification = () => {
    setNotification(null);
  };

  // Handle show/hide steps
  const handleToggleSteps = () => {
    setShowSteps(prev => !prev);
  };

  return (
    <div className="container">
      {/* Header */}
      <div className="text-center mb-3">
        <h1 style={{ 
          color: 'white', 
          textShadow: '2px 2px 4px rgba(0,0,0,0.3)',
          marginBottom: '10px'
        }}>
          🧮 GPTB2 - Giải Phương Trình Bậc 2
        </h1>
        <p style={{ 
          color: 'rgba(255,255,255,0.9)', 
          fontSize: '18px',
          textShadow: '1px 1px 2px rgba(0,0,0,0.3)'
        }}>
          Ứng dụng giải phương trình bậc hai với React + Flask + MySQL
        </p>
      </div>

      {/* API Status */}
      <div className="card">
        <h3>🔌 Trạng thái kết nối API</h3>
        <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
          {apiStatus === 'checking' && (
            <>
              <span className="loading"></span>
              <span>Đang kiểm tra kết nối...</span>
            </>
          )}
          {apiStatus === 'connected' && (
            <>
              <span style={{ color: '#28a745', fontSize: '20px' }}>✅</span>
              <span style={{ color: '#28a745', fontWeight: 'bold' }}>
                Kết nối thành công đến Backend API
              </span>
            </>
          )}
          {apiStatus === 'error' && (
            <>
              <span style={{ color: '#dc3545', fontSize: '20px' }}>❌</span>
              <span style={{ color: '#dc3545', fontWeight: 'bold' }}>
                Không thể kết nối đến Backend API
              </span>
              <button 
                onClick={checkApiConnection}
                className="btn"
                style={{ 
                  background: '#17a2b8', 
                  color: 'white',
                  marginLeft: '10px',
                  padding: '5px 15px',
                  fontSize: '14px'
                }}
              >
                🔄 Thử lại
              </button>
            </>
          )}
        </div>
        
        <div style={{ 
          fontSize: '14px', 
          color: '#666', 
          marginTop: '10px',
          padding: '10px',
          background: '#f8f9fa',
          borderRadius: '5px'
        }}>
          <strong>API Endpoint:</strong> {process.env.REACT_APP_API_URL || 'http://localhost:5000'}
        </div>
      </div>

      {/* Notification */}
      {notification && (
        <div className={`alert alert-${notification.type}`} style={{ position: 'relative' }}>
          {notification.message}
          <button
            onClick={clearNotification}
            style={{
              position: 'absolute',
              right: '10px',
              top: '50%',
              transform: 'translateY(-50%)',
              background: 'none',
              border: 'none',
              fontSize: '18px',
              cursor: 'pointer',
              opacity: 0.7
            }}
          >
            ×
          </button>
        </div>
      )}

      {/* Main Form */}
      <EquationForm 
        onEquationCreated={handleEquationCreated}
        onError={handleError}
      />

      {/* Current Equation Result - Enhanced Display */}
      {currentEquation && (
        <EquationResult
          equation={currentEquation}
          showSteps={showSteps}
          onShowSteps={handleToggleSteps}
        />
      )}

      {/* Recently Created Equations - Compact List */}
      {createdEquations.length > 1 && (
        <div className="card">
          <h3 style={{ 
            display: 'flex', 
            alignItems: 'center', 
            gap: '10px',
            color: '#495057'
          }}>
            📋 Lịch sử phương trình ({createdEquations.length})
          </h3>
          <div style={{ maxHeight: '300px', overflowY: 'auto' }}>
            {createdEquations.slice(1).map((equation, index) => (
              <div 
                key={equation.id || index}
                style={{
                  padding: '12px 15px',
                  margin: '8px 0',
                  background: '#f8f9fa',
                  borderRadius: '8px',
                  borderLeft: '4px solid #667eea',
                  cursor: 'pointer',
                  transition: 'all 0.2s ease'
                }}
                onClick={() => {
                  setCurrentEquation(equation);
                  setShowSteps(false);
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.background = '#e9ecef';
                  e.currentTarget.style.transform = 'translateX(5px)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.background = '#f8f9fa';
                  e.currentTarget.style.transform = 'translateX(0)';
                }}
              >
                <div style={{ 
                  fontSize: '14px', 
                  fontWeight: 'bold',
                  color: '#2c3e50',
                  marginBottom: '5px'
                }}>
                  📝 {equation.equation_string}
                </div>
                <div style={{ 
                  fontSize: '13px', 
                  color: '#666',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center'
                }}>
                  <span>
                    ID: {equation.id} | 
                    Loại: {equation.solution_type} | 
                    Δ: {equation.discriminant?.toFixed(2)}
                  </span>
                  <span style={{ 
                    fontSize: '12px',
                    color: '#999'
                  }}>
                    {equation.created_at ? 
                      new Date(equation.created_at).toLocaleString('vi-VN') : 
                      'N/A'
                    }
                  </span>
                </div>
              </div>
            ))}
          </div>
          <div style={{
            textAlign: 'center',
            marginTop: '15px',
            fontSize: '14px',
            color: '#666'
          }}>
            💡 Click vào phương trình để xem chi tiết
          </div>
        </div>
      )}

      {/* Footer */}
      <div className="text-center" style={{ 
        color: 'rgba(255,255,255,0.8)', 
        marginTop: '30px',
        textShadow: '1px 1px 2px rgba(0,0,0,0.3)'
      }}>
        <p>🚀 GPTB2 v1.0 - React + TypeScript + Flask + MySQL</p>
        <p style={{ fontSize: '14px' }}>
          Task 2.2: Enhanced result display với step-by-step solution ✅
        </p>
      </div>
    </div>
  );
};

export default App;