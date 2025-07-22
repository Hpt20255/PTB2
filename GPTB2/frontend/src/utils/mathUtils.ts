// Mathematical utilities for equation formatting and calculations

export interface QuadraticCoefficients {
  a: number;
  b: number;
  c: number;
}

export interface SolutionResult {
  type: 'two_real' | 'one_real' | 'complex' | 'linear' | 'infinite' | 'none';
  discriminant: number;
  solutions: number[] | { real: number; imaginary: number }[];
  steps: string[];
}

/**
 * Format equation coefficients into mathematical expression
 */
export const formatEquationString = (a: number, b: number, c: number): string => {
  let parts: string[] = [];
  
  // Handle a coefficient (x²)
  if (a !== 0) {
    if (a === 1) {
      parts.push('x²');
    } else if (a === -1) {
      parts.push('-x²');
    } else {
      parts.push(`${a}x²`);
    }
  }
  
  // Handle b coefficient (x)
  if (b !== 0) {
    let bTerm = '';
    if (b === 1) {
      bTerm = 'x';
    } else if (b === -1) {
      bTerm = '-x';
    } else {
      bTerm = `${b}x`;
    }
    
    if (parts.length > 0) {
      if (b > 0) {
        parts.push(`+ ${bTerm.replace('-', '')}`);
      } else {
        parts.push(`- ${bTerm.replace('-', '')}`);
      }
    } else {
      parts.push(bTerm);
    }
  }
  
  // Handle c coefficient (constant)
  if (c !== 0) {
    if (parts.length > 0) {
      if (c > 0) {
        parts.push(`+ ${c}`);
      } else {
        parts.push(`- ${Math.abs(c)}`);
      }
    } else {
      parts.push(`${c}`);
    }
  }
  
  // Handle special case where all coefficients result in empty parts
  if (parts.length === 0) {
    return '0 = 0';
  }
  
  return `${parts.join(' ')} = 0`;
};

/**
 * Format solution for display
 */
export const formatSolution = (
  type: string,
  solutions: number[] | { real: number; imaginary: number }[],
  precision: number = 6
): string => {
  switch (type) {
    case 'two_real':
      const [x1, x2] = solutions as number[];
      return `x₁ = ${x1.toFixed(precision)}, x₂ = ${x2.toFixed(precision)}`;
    
    case 'one_real':
      const [x] = solutions as number[];
      return `x = ${x.toFixed(precision)} (nghiệm kép)`;
    
    case 'complex':
      const [sol1, sol2] = solutions as { real: number; imaginary: number }[];
      return `x₁ = ${sol1.real.toFixed(precision)} + ${sol1.imaginary.toFixed(precision)}i, x₂ = ${sol2.real.toFixed(precision)} - ${sol2.imaginary.toFixed(precision)}i`;
    
    case 'linear':
      const [linearX] = solutions as number[];
      return `x = ${linearX.toFixed(precision)}`;
    
    case 'infinite':
      return 'Vô số nghiệm (phương trình đồng nhất)';
    
    case 'none':
      return 'Vô nghiệm';
    
    default:
      return 'Không xác định';
  }
};

/**
 * Get solution type information
 */
export const getSolutionTypeInfo = (type: string) => {
  const typeMap = {
    'two_real': {
      icon: '🎯',
      color: '#28a745',
      name: 'Hai nghiệm thực phân biệt',
      condition: 'Δ > 0',
      description: 'Phương trình có hai nghiệm thực khác nhau'
    },
    'one_real': {
      icon: '🎪',
      color: '#ffc107',
      name: 'Một nghiệm thực (nghiệm kép)',
      condition: 'Δ = 0',
      description: 'Phương trình có một nghiệm thực với bội số 2'
    },
    'complex': {
      icon: '🌀',
      color: '#6f42c1',
      name: 'Hai nghiệm phức',
      condition: 'Δ < 0',
      description: 'Phương trình có hai nghiệm phức liên hợp'
    },
    'linear': {
      icon: '📏',
      color: '#17a2b8',
      name: 'Phương trình bậc nhất',
      condition: 'a = 0, b ≠ 0',
      description: 'Phương trình tuyến tính một ẩn'
    },
    'infinite': {
      icon: '♾️',
      color: '#6c757d',
      name: 'Vô số nghiệm',
      condition: 'a = b = c = 0',
      description: 'Phương trình đồng nhất, mọi số thực đều là nghiệm'
    },
    'none': {
      icon: '❌',
      color: '#dc3545',
      name: 'Vô nghiệm',
      condition: 'a = 0, b = 0, c ≠ 0',
      description: 'Phương trình vô nghiệm'
    }
  };
  
  return typeMap[type as keyof typeof typeMap] || {
    icon: '❓',
    color: '#6c757d',
    name: 'Không xác định',
    condition: '',
    description: 'Loại nghiệm không được nhận dạng'
  };
};

/**
 * Generate step-by-step solution
 */
export const generateSolutionSteps = (a: number, b: number, c: number): string[] => {
  const steps: string[] = [];
  
  if (a === 0) {
    // Linear or degenerate case
    if (b === 0) {
      if (c === 0) {
        steps.push('🔍 Phân tích phương trình:');
        steps.push('Phương trình có dạng 0 = 0');
        steps.push('✅ Đây là phương trình đồng nhất');
        steps.push('🎯 Kết luận: Phương trình có vô số nghiệm');
      } else {
        steps.push('🔍 Phân tích phương trình:');
        steps.push(`Phương trình có dạng ${c} = 0`);
        steps.push('❌ Đây là phương trình vô nghiệm');
        steps.push('🎯 Kết luận: Phương trình vô nghiệm');
      }
    } else {
      steps.push('🔍 Phân tích phương trình:');
      steps.push('Hệ số a = 0, đây là phương trình bậc nhất');
      steps.push(`📝 Phương trình: ${b}x + ${c} = 0`);
      steps.push('🔧 Giải phương trình bậc nhất:');
      steps.push(`${b}x = ${-c}`);
      steps.push(`x = ${-c}/${b}`);
      steps.push(`🎯 Nghiệm: x = ${(-c/b).toFixed(6)}`);
    }
  } else {
    // Quadratic equation
    const discriminant = b * b - 4 * a * c;
    
    steps.push('🔍 Phân tích phương trình bậc hai:');
    steps.push(`📝 Phương trình: ${formatEquationString(a, b, c)}`);
    steps.push(`📊 Hệ số: a = ${a}, b = ${b}, c = ${c}`);
    steps.push('');
    steps.push('🧮 Tính biệt thức Δ:');
    steps.push('Δ = b² - 4ac');
    steps.push(`Δ = (${b})² - 4(${a})(${c})`);
    steps.push(`Δ = ${b * b} - ${4 * a * c}`);
    steps.push(`Δ = ${discriminant}`);
    steps.push('');
    
    if (discriminant > 0) {
      const sqrtDelta = Math.sqrt(discriminant);
      steps.push('✅ Δ > 0: Phương trình có hai nghiệm thực phân biệt');
      steps.push('🔧 Áp dụng công thức nghiệm:');
      steps.push('x₁ = (-b + √Δ)/(2a)');
      steps.push('x₂ = (-b - √Δ)/(2a)');
      steps.push('');
      steps.push(`√Δ = √${discriminant} = ${sqrtDelta.toFixed(6)}`);
      steps.push('');
      steps.push('🎯 Tính nghiệm x₁:');
      steps.push(`x₁ = (${-b} + ${sqrtDelta.toFixed(6)})/(2 × ${a})`);
      steps.push(`x₁ = ${(-b + sqrtDelta).toFixed(6)}/${2 * a}`);
      steps.push(`x₁ = ${((-b + sqrtDelta) / (2 * a)).toFixed(6)}`);
      steps.push('');
      steps.push('🎯 Tính nghiệm x₂:');
      steps.push(`x₂ = (${-b} - ${sqrtDelta.toFixed(6)})/(2 × ${a})`);
      steps.push(`x₂ = ${(-b - sqrtDelta).toFixed(6)}/${2 * a}`);
      steps.push(`x₂ = ${((-b - sqrtDelta) / (2 * a)).toFixed(6)}`);
      
    } else if (discriminant === 0) {
      steps.push('✅ Δ = 0: Phương trình có nghiệm kép');
      steps.push('🔧 Áp dụng công thức nghiệm:');
      steps.push('x = -b/(2a)');
      steps.push('');
      steps.push('🎯 Tính nghiệm:');
      steps.push(`x = ${-b}/(2 × ${a})`);
      steps.push(`x = ${-b}/${2 * a}`);
      steps.push(`x = ${(-b / (2 * a)).toFixed(6)}`);
      
    } else {
      const sqrtAbsDelta = Math.sqrt(Math.abs(discriminant));
      const realPart = -b / (2 * a);
      const imagPart = sqrtAbsDelta / (2 * a);
      
      steps.push('✅ Δ < 0: Phương trình có hai nghiệm phức');
      steps.push('🔧 Áp dụng công thức nghiệm phức:');
      steps.push('x₁ = (-b + i√|Δ|)/(2a)');
      steps.push('x₂ = (-b - i√|Δ|)/(2a)');
      steps.push('');
      steps.push(`|Δ| = ${Math.abs(discriminant)}`);
      steps.push(`√|Δ| = ${sqrtAbsDelta.toFixed(6)}`);
      steps.push('');
      steps.push('🎯 Tính nghiệm x₁:');
      steps.push(`x₁ = (${-b} + i × ${sqrtAbsDelta.toFixed(6)})/(2 × ${a})`);
      steps.push(`x₁ = ${realPart.toFixed(6)} + ${imagPart.toFixed(6)}i`);
      steps.push('');
      steps.push('🎯 Tính nghiệm x₂:');
      steps.push(`x₂ = (${-b} - i × ${sqrtAbsDelta.toFixed(6)})/(2 × ${a})`);
      steps.push(`x₂ = ${realPart.toFixed(6)} - ${imagPart.toFixed(6)}i`);
    }
  }
  
  return steps;
};

/**
 * Validate equation coefficients
 */
export const validateCoefficients = (a: any, b: any, c: any): { valid: boolean; errors: string[] } => {
  const errors: string[] = [];
  
  if (a === undefined || a === null || a === '') {
    errors.push('Hệ số a không được để trống');
  } else if (isNaN(Number(a))) {
    errors.push('Hệ số a phải là một số');
  }
  
  if (b === undefined || b === null || b === '') {
    errors.push('Hệ số b không được để trống');
  } else if (isNaN(Number(b))) {
    errors.push('Hệ số b phải là một số');
  }
  
  if (c === undefined || c === null || c === '') {
    errors.push('Hệ số c không được để trống');
  } else if (isNaN(Number(c))) {
    errors.push('Hệ số c phải là một số');
  }
  
  return {
    valid: errors.length === 0,
    errors
  };
};

/**
 * Format number for display
 */
export const formatNumber = (num: number, precision: number = 6): string => {
  if (Number.isInteger(num)) {
    return num.toString();
  }
  return num.toFixed(precision).replace(/\.?0+$/, '');
};