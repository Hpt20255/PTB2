"""
Database models for GPTB2 application
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Equation(db.Model):
    """
    Model for storing quadratic equations and their solutions
    Represents: ax² + bx + c = 0
    """
    __tablename__ = 'equations'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    a = db.Column(db.Float, nullable=False, comment='Coefficient of x²')
    b = db.Column(db.Float, nullable=False, comment='Coefficient of x')
    c = db.Column(db.Float, nullable=False, comment='Constant term')
    solution = db.Column(db.String(200), nullable=True, comment='Solution as string')
    discriminant = db.Column(db.Float, nullable=True, comment='b² - 4ac')
    solution_type = db.Column(db.String(50), nullable=True, comment='Type: two_real, one_real, complex')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment='Creation timestamp')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, comment='Last update timestamp')
    
    def __init__(self, a, b, c):
        """Initialize equation with coefficients"""
        self.a = float(a)
        self.b = float(b) 
        self.c = float(c)
        self.solve_equation()
    
    def solve_equation(self):
        """Solve quadratic equation and store results"""
        import math
        
        # Handle case where a = 0 (not quadratic)
        if self.a == 0:
            if self.b == 0:
                if self.c == 0:
                    self.solution = "Infinite solutions (0 = 0)"
                    self.solution_type = "infinite"
                else:
                    self.solution = "No solution (contradiction)"
                    self.solution_type = "none"
            else:
                # Linear equation: bx + c = 0
                x = -self.c / self.b
                self.solution = f"x = {x:.6f}"
                self.solution_type = "linear"
            self.discriminant = None
            return
        
        # Calculate discriminant
        self.discriminant = self.b**2 - 4*self.a*self.c
        
        if self.discriminant > 0:
            # Two distinct real roots
            sqrt_discriminant = math.sqrt(self.discriminant)
            x1 = (-self.b + sqrt_discriminant) / (2 * self.a)
            x2 = (-self.b - sqrt_discriminant) / (2 * self.a)
            self.solution = f"x₁ = {x1:.6f}, x₂ = {x2:.6f}"
            self.solution_type = "two_real"
            
        elif self.discriminant == 0:
            # One repeated real root
            x = -self.b / (2 * self.a)
            self.solution = f"x = {x:.6f} (repeated root)"
            self.solution_type = "one_real"
            
        else:
            # Complex roots
            real_part = -self.b / (2 * self.a)
            imaginary_part = math.sqrt(-self.discriminant) / (2 * self.a)
            self.solution = f"x₁ = {real_part:.6f} + {imaginary_part:.6f}i, x₂ = {real_part:.6f} - {imaginary_part:.6f}i"
            self.solution_type = "complex"
    
    def to_dict(self):
        """Convert model to dictionary for JSON serialization"""
        return {
            'id': self.id,
            'a': self.a,
            'b': self.b,
            'c': self.c,
            'solution': self.solution,
            'discriminant': self.discriminant,
            'solution_type': self.solution_type,
            'equation_string': f"{self.a}x² + {self.b}x + {self.c} = 0",
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    def __repr__(self):
        """String representation of the equation"""
        return f"<Equation {self.a}x² + {self.b}x + {self.c} = 0, Solution: {self.solution}>"