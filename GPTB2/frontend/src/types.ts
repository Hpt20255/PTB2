// Type definitions for GPTB2 application

export interface EquationData {
  id?: number;
  a: number;
  b: number;
  c: number;
  solution?: string;
  discriminant?: number;
  solution_type?: string;
  equation_string?: string;
  created_at?: string;
  updated_at?: string;
}

export interface ApiResponse<T> {
  message: string;
  status: 'success' | 'error' | 'partial_success';
  data?: T;
  error?: string;
  database_error?: string;
}

export interface EquationFormData {
  a: string;
  b: string;
  c: string;
}

export interface ValidationError {
  field: string;
  message: string;
}

export type SolutionType = 'two_real' | 'one_real' | 'complex' | 'linear' | 'infinite' | 'none';