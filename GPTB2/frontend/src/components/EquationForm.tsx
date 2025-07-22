import React, { useState } from 'react';
import { EquationFormData, EquationData, ValidationError } from '../types';
import { equationApi } from '../services/api';

interface EquationFormProps {
  onEquationCreated?: (equation: EquationData) => void;
  onError?: (error: string) => void;
}

const EquationForm: React.FC<EquationFormProps> = ({ onEquationCreated, onError }) => {
  const [formData, setFormData] = useState<EquationFormData>({
    a: '',
    b: '',
    c: ''
  });
  
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<EquationData | null>(null);
  const [error, setError] = useState<string>('');
  const [validationErrors, setValidationErrors] = useState<ValidationError[]>([]);

  // Validate form data
  const validateForm = (): ValidationError[] => {
    const errors: ValidationError[] = [];
    
    if (!formData.a.trim()) {
      errors.push({ field: 'a', message: 'Hệ số a không được để trống' });
    } else if (isNaN(Number(formData.a))) {
      errors.push({ field: 'a', message: 'Hệ số a phải là một số' });
    }
    
    if (!formData.b.trim()) {
      errors.push({ field: 'b', message: 'Hệ số b không được để trống' });
    } else if (isNaN(Number(formData.b))) {
      errors.push({ field: 'b', message: 'Hệ số b phải là một số' });
    }
    
    if (!formData.c.trim()) {
      errors.push({ field: 'c', message: 'Hệ số c không được để trống' });
    } else if (isNaN(Number(formData.c))) {
      errors.push({ field: 'c', message: 'Hệ số c phải là một số' });
    }
    
    return errors;
  };

  // Handle input changes
  const handleInputChange = (field: keyof EquationFormData, value: string) => {
    setFormData(prev => ({
      ...prev,
      [field]: value
    }));
    
    // Clear validation errors for this field
    setValidationErrors(prev => prev.filter(error => error.field !== field));
    
    // Clear general error
    if (error) setError('');
  };

  // Handle form submission
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    // Validate form
    const errors = validateForm();
    if (errors.length > 0) {
      setValidationErrors(errors);
      return;
    }
    
    setLoading(true);
    setError('');
    setResult(null);
    
    try {
      // Convert form data to numbers
      const coefficients = {
        a: Number(formData.a),
        b: Number(formData.b),
        c: Number(formData.c)
      };
      
      console.log('🧮 Submitting equation:', coefficients);
      
      // Call API
      const response = await equationApi.create(coefficients);
      
      if (response.status === 'success' || response.status === 'partial_success') {
        setResult(response.data!);
        
        // Call callback if provided
        if (onEquationCreated && response.data) {
          onEquationCreated(response.data);
        }
        
        // Show success message
        console.log('✅ Equation created successfully:', response.data);
        
        // Clear form after successful submission
        setFormData({ a: '', b: '', c: '' });
        
      } else {
        const errorMessage = response.error || response.message || 'Có lỗi xảy ra khi tạo phương trình';
        setError(errorMessage);
        
        if (onError) {
          onError(errorMessage);
        }
      }
      
    } catch (err: any) {
      const errorMessage = err.message || 'Không thể kết nối đến server';
      setError(errorMessage);
      
      if (onError) {
        onError(errorMessage);
      }
      
      console.error('❌ Error creating equation:', err);
    } finally {
      setLoading(false);
    }
  };

  // Clear form
  const handleClear = () => {
    setFormData({ a: '', b: '', c: '' });
    setResult(null);
    setError('');
    setValidationErrors([]);
  };

  // Get validation error for field
  const getFieldError = (field: string): string | undefined => {
    return validationErrors.find(error => error.field === field)?.message;
  };

  return (
    <div className="card">
      <h2 className="text-center mb-3">🧮 Giải Phương Trình Bậc 2</h2>
      <p className="text-center mb-3" style={{ color: '#666' }}>
        Nhập các hệ số a, b, c của phương trình ax² + bx + c = 0
      </p>
      
      <form onSubmit={handleSubmit}>
        {/* Coefficient A */}
        <div className="form-group">
          <label htmlFor="coefficient-a">
            Hệ số a (x²): <span style={{ color: 'red' }}>*</span>
          </label>
          <input
            id="coefficient-a"
            type="text"
            value={formData.a}
            onChange={(e) => handleInputChange('a', e.target.value)}
            placeholder="Nhập hệ số a (ví dụ: 1)"
            disabled={loading}
            style={{
              borderColor: getFieldError('a') ? '#dc3545' : undefined
            }}
          />
          {getFieldError('a') && (
            <div style={{ color: '#dc3545', fontSize: '14px', marginTop: '5px' }}>
              {getFieldError('a')}
            </div>
          )}
        </div>

        {/* Coefficient B */}
        <div className="form-group">
          <label htmlFor="coefficient-b">
            Hệ số b (x): <span style={{ color: 'red' }}>*</span>
          </label>
          <input
            id="coefficient-b"
            type="text"
            value={formData.b}
            onChange={(e) => handleInputChange('b', e.target.value)}
            placeholder="Nhập hệ số b (ví dụ: -5)"
            disabled={loading}
            style={{
              borderColor: getFieldError('b') ? '#dc3545' : undefined
            }}
          />
          {getFieldError('b') && (
            <div style={{ color: '#dc3545', fontSize: '14px', marginTop: '5px' }}>
              {getFieldError('b')}
            </div>
          )}
        </div>

        {/* Coefficient C */}
        <div className="form-group">
          <label htmlFor="coefficient-c">
            Hệ số c (hằng số): <span style={{ color: 'red' }}>*</span>
          </label>
          <input
            id="coefficient-c"
            type="text"
            value={formData.c}
            onChange={(e) => handleInputChange('c', e.target.value)}
            placeholder="Nhập hệ số c (ví dụ: 6)"
            disabled={loading}
            style={{
              borderColor: getFieldError('c') ? '#dc3545' : undefined
            }}
          />
          {getFieldError('c') && (
            <div style={{ color: '#dc3545', fontSize: '14px', marginTop: '5px' }}>
              {getFieldError('c')}
            </div>
          )}
        </div>

        {/* Buttons */}
        <div className="text-center">
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading}
            style={{ marginRight: '10px' }}
          >
            {loading && <span className="loading"></span>}
            {loading ? 'Đang giải...' : '🚀 Giải Phương Trình'}
          </button>
          
          <button
            type="button"
            onClick={handleClear}
            className="btn"
            disabled={loading}
            style={{
              background: '#6c757d',
              color: 'white'
            }}
          >
            🗑️ Xóa
          </button>
        </div>
      </form>

      {/* Error Display */}
      {error && (
        <div className="alert alert-error mt-3">
          <strong>❌ Lỗi:</strong> {error}
        </div>
      )}

      {/* Result Display */}
      {result && (
        <div className="alert alert-success mt-3">
          <h3>✅ Kết quả:</h3>
          <div className="equation-display">
            📝 Phương trình: {result.equation_string}
          </div>
          <div className="solution-display">
            🎯 Nghiệm: {result.solution}
          </div>
          <div style={{ fontSize: '14px', color: '#666', marginTop: '10px' }}>
            📊 Loại nghiệm: {result.solution_type} | 
            Δ = {result.discriminant} | 
            ID: {result.id}
          </div>
        </div>
      )}
    </div>
  );
};

export default EquationForm;