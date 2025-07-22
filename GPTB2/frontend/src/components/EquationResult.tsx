import React from 'react';
import { EquationData, SolutionType } from '../types';

interface EquationResultProps {
  equation: EquationData;
  showSteps?: boolean;
  onShowSteps?: () => void;
}

const EquationResult: React.FC<EquationResultProps> = ({ 
  equation, 
  showSteps = false, 
  onShowSteps 
}) => {
  // Get solution type info
  const getSolutionTypeInfo = (type: string) => {
    switch (type) {
      case 'two_real':
        return {
          icon: '🎯',
          color: '#28a745',
          description: 'Hai nghiệm thực phân biệt',
          condition: 'Δ > 0'
        };
      case 'one_real':
        return {
          icon: '🎪',
          color: '#ffc107',
          description: 'Một nghiệm thực (nghiệm kép)',
          condition: 'Δ = 0'
        };
      case 'complex':
        return {
          icon: '🌀',
          color: '#6f42c1',
          description: 'Hai nghiệm phức',
          condition: 'Δ < 0'
        };
      case 'linear':
        return {
          icon: '📏',
          color: '#17a2b8',
          description: 'Phương trình bậc nhất',
          condition: 'a = 0, b ≠ 0'
        };
      case 'infinite':
        return {
          icon: '♾️',
          color: '#6c757d',
          description: 'Vô số nghiệm',
          condition: 'a = b = c = 0'
        };
      case 'none':
        return {
          icon: '❌',
          color: '#dc3545',
          description: 'Vô nghiệm',
          condition: 'a = 0, b = 0, c ≠ 0'
        };
      default:
        return {
          icon: '❓',
          color: '#6c757d',
          description: 'Không xác định',
          condition: ''
        };
    }
  };

  // Format mathematical expression
  const formatEquation = (a: number, b: number, c: number): string => {
    let equation = '';
    
    // Handle coefficient a
    if (a !== 0) {
      if (a === 1) {
        equation += 'x²';
      } else if (a === -1) {
        equation += '-x²';
      } else {
        equation += `${a}x²`;
      }
    }
    
    // Handle coefficient b
    if (b !== 0) {
      if (equation && b > 0) {
        equation += ' + ';
      } else if (equation && b < 0) {
        equation += ' - ';
        b = Math.abs(b);
      }
      
      if (b === 1 && equation) {
        equation += 'x';
      } else if (b === 1 && !equation) {
        equation += 'x';
      } else {
        equation += `${b}x`;
      }
    }
    
    // Handle coefficient c
    if (c !== 0) {
      if (equation && c > 0) {
        equation += ` + ${c}`;
      } else if (equation && c < 0) {
        equation += ` - ${Math.abs(c)}`;
      } else {
        equation += `${c}`;
      }
    }
    
    // Handle special cases
    if (!equation) {
      equation = '0';
    }
    
    return `${equation} = 0`;
  };

  // Generate solution steps
  const generateSolutionSteps = () => {
    const { a, b, c, discriminant } = equation;
    const steps = [];

    if (a === 0) {
      // Linear equation
      if (b === 0) {
        if (c === 0) {
          steps.push('Phương trình có dạng 0 = 0, nên có vô số nghiệm.');
        } else {
          steps.push(`Phương trình có dạng ${c} = 0, vô nghiệm.`);
        }
      } else {
        steps.push('Đây là phương trình bậc nhất:');
        steps.push(`${b}x + ${c} = 0`);
        steps.push(`${b}x = ${-c}`);
        steps.push(`x = ${-c}/${b} = ${(-c/b).toFixed(6)}`);
      }
    } else {
      // Quadratic equation
      steps.push('Đây là phương trình bậc hai, áp dụng công thức nghiệm:');
      steps.push(`Δ = b² - 4ac = (${b})² - 4(${a})(${c})`);
      steps.push(`Δ = ${b*b} - ${4*a*c} = ${discriminant}`);
      
      if (discriminant! > 0) {
        const sqrtDelta = Math.sqrt(discriminant!);
        steps.push(`√Δ = √${discriminant} = ${sqrtDelta.toFixed(6)}`);
        steps.push('Phương trình có hai nghiệm phân biệt:');
        steps.push(`x₁ = (-b + √Δ)/(2a) = (${-b} + ${sqrtDelta.toFixed(6)})/(2×${a}) = ${((-b + sqrtDelta)/(2*a)).toFixed(6)}`);
        steps.push(`x₂ = (-b - √Δ)/(2a) = (${-b} - ${sqrtDelta.toFixed(6)})/(2×${a}) = ${((-b - sqrtDelta)/(2*a)).toFixed(6)}`);
      } else if (discriminant === 0) {
        steps.push('Δ = 0, phương trình có nghiệm kép:');
        steps.push(`x = -b/(2a) = ${-b}/(2×${a}) = ${(-b/(2*a)).toFixed(6)}`);
      } else {
        const sqrtAbsDelta = Math.sqrt(Math.abs(discriminant!));
        steps.push(`Δ < 0, phương trình có hai nghiệm phức:');
        steps.push(`x₁ = (-b + i√|Δ|)/(2a) = (${-b} + i×${sqrtAbsDelta.toFixed(6)})/(2×${a})`);
        steps.push(`x₂ = (-b - i√|Δ|)/(2a) = (${-b} - i×${sqrtAbsDelta.toFixed(6)})/(2×${a})`);
        
        const realPart = -b / (2 * a);
        const imagPart = sqrtAbsDelta / (2 * a);
        steps.push(`x₁ = ${realPart.toFixed(6)} + ${imagPart.toFixed(6)}i`);
        steps.push(`x₂ = ${realPart.toFixed(6)} - ${imagPart.toFixed(6)}i`);
      }
    }

    return steps;
  };

  const solutionInfo = getSolutionTypeInfo(equation.solution_type || '');
  const formattedEquation = formatEquation(equation.a, equation.b, equation.c);
  const solutionSteps = generateSolutionSteps();

  return (
    <div className="equation-result-container">
      {/* Main Result Card */}
      <div className="card result-card">
        <div className="result-header">
          <h3 style={{ 
            color: solutionInfo.color,
            display: 'flex',
            alignItems: 'center',
            gap: '10px',
            margin: 0
          }}>
            <span style={{ fontSize: '24px' }}>{solutionInfo.icon}</span>
            Kết quả giải phương trình
          </h3>
        </div>

        {/* Equation Display */}
        <div className="equation-display-enhanced">
          <div className="equation-label">📝 Phương trình:</div>
          <div className="equation-math" style={{
            fontSize: '20px',
            fontWeight: 'bold',
            color: '#2c3e50',
            background: '#f8f9fa',
            padding: '15px',
            borderRadius: '8px',
            textAlign: 'center',
            fontFamily: 'Courier New, monospace',
            border: '2px solid #e9ecef'
          }}>
            {formattedEquation}
          </div>
        </div>

        {/* Solution Display */}
        <div className="solution-display-enhanced">
          <div className="solution-label">🎯 Nghiệm:</div>
          <div className="solution-math" style={{
            fontSize: '18px',
            fontWeight: 'bold',
            color: solutionInfo.color,
            background: `${solutionInfo.color}10`,
            padding: '15px',
            borderRadius: '8px',
            textAlign: 'center',
            fontFamily: 'Courier New, monospace',
            border: `2px solid ${solutionInfo.color}30`
          }}>
            {equation.solution}
          </div>
        </div>

        {/* Solution Type Info */}
        <div className="solution-type-info" style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          padding: '15px',
          background: '#f8f9fa',
          borderRadius: '8px',
          margin: '15px 0'
        }}>
          <div>
            <div style={{ 
              fontWeight: 'bold', 
              color: solutionInfo.color,
              fontSize: '16px'
            }}>
              {solutionInfo.icon} {solutionInfo.description}
            </div>
            <div style={{ 
              fontSize: '14px', 
              color: '#666',
              marginTop: '5px'
            }}>
              Điều kiện: {solutionInfo.condition}
            </div>
          </div>
          <div style={{
            background: solutionInfo.color,
            color: 'white',
            padding: '8px 15px',
            borderRadius: '20px',
            fontSize: '14px',
            fontWeight: 'bold'
          }}>
            Δ = {equation.discriminant?.toFixed(2)}
          </div>
        </div>

        {/* Action Buttons */}
        <div className="result-actions" style={{
          display: 'flex',
          gap: '10px',
          justifyContent: 'center',
          marginTop: '20px'
        }}>
          <button
            onClick={onShowSteps}
            className="btn"
            style={{
              background: '#17a2b8',
              color: 'white',
              border: 'none',
              padding: '10px 20px',
              borderRadius: '8px',
              cursor: 'pointer',
              fontSize: '14px',
              fontWeight: 'bold'
            }}
          >
            📚 {showSteps ? 'Ẩn' : 'Xem'} lời giải chi tiết
          </button>
        </div>
      </div>

      {/* Solution Steps */}
      {showSteps && (
        <div className="card solution-steps-card">
          <h4 style={{ 
            color: '#495057',
            marginBottom: '20px',
            display: 'flex',
            alignItems: 'center',
            gap: '10px'
          }}>
            📚 Lời giải chi tiết
          </h4>
          
          <div className="solution-steps">
            {solutionSteps.map((step, index) => (
              <div 
                key={index}
                className="solution-step"
                style={{
                  padding: '12px 15px',
                  margin: '8px 0',
                  background: index === 0 ? '#e3f2fd' : '#f8f9fa',
                  borderLeft: `4px solid ${index === 0 ? '#2196f3' : '#dee2e6'}`,
                  borderRadius: '0 8px 8px 0',
                  fontSize: '15px',
                  lineHeight: '1.5'
                }}
              >
                <span style={{ 
                  fontWeight: 'bold', 
                  color: '#495057',
                  marginRight: '8px'
                }}>
                  {index + 1}.
                </span>
                {step}
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Additional Info */}
      <div className="card additional-info-card">
        <h4 style={{ 
          color: '#495057',
          marginBottom: '15px',
          fontSize: '16px'
        }}>
          📊 Thông tin bổ sung
        </h4>
        
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
          gap: '15px'
        }}>
          <div className="info-item">
            <div style={{ fontWeight: 'bold', color: '#666', fontSize: '14px' }}>
              Hệ số a (x²)
            </div>
            <div style={{ fontSize: '16px', color: '#2c3e50' }}>
              {equation.a}
            </div>
          </div>
          
          <div className="info-item">
            <div style={{ fontWeight: 'bold', color: '#666', fontSize: '14px' }}>
              Hệ số b (x)
            </div>
            <div style={{ fontSize: '16px', color: '#2c3e50' }}>
              {equation.b}
            </div>
          </div>
          
          <div className="info-item">
            <div style={{ fontWeight: 'bold', color: '#666', fontSize: '14px' }}>
              Hệ số c (hằng số)
            </div>
            <div style={{ fontSize: '16px', color: '#2c3e50' }}>
              {equation.c}
            </div>
          </div>
          
          <div className="info-item">
            <div style={{ fontWeight: 'bold', color: '#666', fontSize: '14px' }}>
              Biệt thức Δ
            </div>
            <div style={{ 
              fontSize: '16px', 
              color: solutionInfo.color,
              fontWeight: 'bold'
            }}>
              {equation.discriminant?.toFixed(6)}
            </div>
          </div>
          
          <div className="info-item">
            <div style={{ fontWeight: 'bold', color: '#666', fontSize: '14px' }}>
              ID phương trình
            </div>
            <div style={{ fontSize: '16px', color: '#2c3e50' }}>
              #{equation.id}
            </div>
          </div>
          
          <div className="info-item">
            <div style={{ fontWeight: 'bold', color: '#666', fontSize: '14px' }}>
              Thời gian tạo
            </div>
            <div style={{ fontSize: '14px', color: '#666' }}>
              {equation.created_at ? 
                new Date(equation.created_at).toLocaleString('vi-VN') : 
                'N/A'
              }
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EquationResult;