#!/usr/bin/env python3
"""
GPTB2 Environment File Merger - Task 4.2
Script to merge all .env files into one consolidated file and detect conflicts
"""

import os
import sys
from pathlib import Path
from collections import defaultdict
import re

def parse_env_file(file_path):
    """Parse .env file and return dictionary of variables"""
    variables = {}
    comments = []
    
    if not file_path.exists():
        return variables, comments
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            
            # Skip empty lines
            if not line:
                continue
            
            # Handle comments
            if line.startswith('#'):
                comments.append(line)
                continue
            
            # Parse variable assignment
            if '=' in line:
                # Handle comments at end of line
                if '#' in line:
                    var_part, comment_part = line.split('#', 1)
                    var_part = var_part.strip()
                    comments.append(f"# {comment_part.strip()}")
                else:
                    var_part = line
                
                # Split variable and value
                key, value = var_part.split('=', 1)
                key = key.strip()
                value = value.strip()
                
                variables[key] = {
                    'value': value,
                    'line': line_num,
                    'original_line': line
                }
    
    return variables, comments

def detect_conflicts(env_files):
    """Detect conflicts between environment variables"""
    all_vars = defaultdict(list)
    conflicts = []
    
    # Collect all variables from all files
    for file_name, (variables, _) in env_files.items():
        for var_name, var_info in variables.items():
            all_vars[var_name].append({
                'file': file_name,
                'value': var_info['value'],
                'line': var_info['line']
            })
    
    # Find conflicts (same variable with different values)
    for var_name, occurrences in all_vars.items():
        if len(occurrences) > 1:
            values = set(occ['value'] for occ in occurrences)
            if len(values) > 1:
                conflicts.append({
                    'variable': var_name,
                    'occurrences': occurrences,
                    'values': list(values)
                })
    
    return conflicts, all_vars

def create_merged_env(env_files, conflicts, all_vars, output_file):
    """Create merged .env file with conflict resolution"""
    
    # Priority order: main -> backend -> frontend
    priority_order = ['.env.main', '.env.backend', '.env.frontend']
    
    merged_vars = {}
    conflict_resolutions = []
    
    # Resolve conflicts based on priority
    for var_name, occurrences in all_vars.items():
        if len(occurrences) == 1:
            # No conflict
            occ = occurrences[0]
            merged_vars[var_name] = {
                'value': occ['value'],
                'source': occ['file'],
                'conflict': False
            }
        else:
            # Conflict - resolve by priority
            best_occ = None
            for priority_file in priority_order:
                for occ in occurrences:
                    if occ['file'] == priority_file:
                        best_occ = occ
                        break
                if best_occ:
                    break
            
            if not best_occ:
                best_occ = occurrences[0]  # Fallback
            
            merged_vars[var_name] = {
                'value': best_occ['value'],
                'source': best_occ['file'],
                'conflict': True
            }
            
            conflict_resolutions.append({
                'variable': var_name,
                'chosen_value': best_occ['value'],
                'chosen_source': best_occ['file'],
                'rejected': [occ for occ in occurrences if occ != best_occ]
            })
    
    # Write merged file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# GPTB2 MERGED ENVIRONMENT VARIABLES - Task 4.2\n")
        f.write("# This file contains all environment variables from main, backend, and frontend .env files\n")
        f.write("# Generated automatically - DO NOT EDIT MANUALLY\n")
        f.write(f"# Generated on: {__import__('datetime').datetime.now().isoformat()}\n")
        f.write("\n")
        
        if conflicts:
            f.write("# CONFLICTS DETECTED AND RESOLVED:\n")
            for resolution in conflict_resolutions:
                f.write(f"# {resolution['variable']}: Using value from {resolution['chosen_source']}\n")
                for rejected in resolution['rejected']:
                    f.write(f"#   Rejected: {rejected['value']} (from {rejected['file']})\n")
            f.write("\n")
        
        # Group variables by category
        categories = {
            'Database Configuration': ['DB_HOST', 'DB_PORT', 'DB_NAME', 'DB_USER', 'DB_PASSWORD'],
            'Application Configuration': ['DEBUG', 'PORT', 'FRONTEND_PORT', 'FLASK_ENV', 'FLASK_DEBUG', 'FLASK_APP'],
            'Security Configuration': ['SECRET_KEY'],
            'API Configuration': ['API_HOST', 'API_PORT', 'CORS_ORIGINS', 'REACT_APP_API_URL', 'REACT_APP_API_TIMEOUT'],
            'Logging Configuration': ['LOG_LEVEL', 'LOG_FORMAT'],
            'SQLAlchemy Configuration': ['SQLALCHEMY_TRACK_MODIFICATIONS', 'SQLALCHEMY_ECHO', 'SQLALCHEMY_POOL_SIZE', 'SQLALCHEMY_POOL_TIMEOUT', 'SQLALCHEMY_POOL_RECYCLE'],
            'React App Configuration': [var for var in merged_vars.keys() if var.startswith('REACT_APP_')],
            'Development Configuration': ['ENABLE_SWAGGER', 'ENABLE_DEBUG_TOOLBAR', 'FAST_REFRESH', 'ESLINT_NO_DEV_ERRORS', 'DISABLE_ESLINT_PLUGIN', 'GENERATE_SOURCEMAP'],
            'Other Configuration': []
        }
        
        # Add uncategorized variables
        categorized_vars = set()
        for cat_vars in categories.values():
            categorized_vars.update(cat_vars)
        
        for var_name in merged_vars.keys():
            if var_name not in categorized_vars:
                categories['Other Configuration'].append(var_name)
        
        # Write variables by category
        for category, var_names in categories.items():
            if not var_names:
                continue
            
            category_vars = [var for var in var_names if var in merged_vars]
            if not category_vars:
                continue
            
            f.write(f"# {category}\n")
            for var_name in sorted(category_vars):
                var_info = merged_vars[var_name]
                conflict_marker = " # CONFLICT RESOLVED" if var_info['conflict'] else ""
                source_marker = f" # from {var_info['source']}"
                f.write(f"{var_name}={var_info['value']}{conflict_marker}{source_marker}\n")
            f.write("\n")
    
    return conflict_resolutions

def main():
    """Main function"""
    print("=" * 70)
    print("🔄 GPTB2 Environment File Merger - Task 4.2")
    print("=" * 70)
    
    # Define file paths
    env_files_paths = {
        '.env.main': Path('.env'),
        '.env.backend': Path('backend/.env'),
        '.env.frontend': Path('frontend/.env')
    }
    
    # Parse all .env files
    print("📁 Parsing environment files...")
    env_files = {}
    for file_key, file_path in env_files_paths.items():
        if file_path.exists():
            variables, comments = parse_env_file(file_path)
            env_files[file_key] = (variables, comments)
            print(f"✅ {file_key}: {len(variables)} variables found")
        else:
            print(f"⚠️  {file_key}: File not found")
            env_files[file_key] = ({}, [])
    
    # Detect conflicts
    print("\n🔍 Detecting conflicts...")
    conflicts, all_vars = detect_conflicts(env_files)
    
    if conflicts:
        print(f"⚠️  Found {len(conflicts)} conflicts:")
        for conflict in conflicts:
            print(f"   🔥 {conflict['variable']}: {len(conflict['occurrences'])} different values")
            for occ in conflict['occurrences']:
                print(f"      - {occ['value']} (from {occ['file']})")
    else:
        print("✅ No conflicts detected")
    
    # Create merged file
    print(f"\n📝 Creating merged .env file...")
    merged_file = Path('.env.merged')
    conflict_resolutions = create_merged_env(env_files, conflicts, all_vars, merged_file)
    
    print(f"✅ Merged file created: {merged_file}")
    print(f"📊 Total variables: {len(all_vars)}")
    print(f"🔥 Conflicts resolved: {len(conflict_resolutions)}")
    
    # Show conflict resolutions
    if conflict_resolutions:
        print("\n🔧 Conflict Resolutions:")
        for resolution in conflict_resolutions:
            print(f"   {resolution['variable']}: {resolution['chosen_value']} (from {resolution['chosen_source']})")
    
    # Create backup of original files
    print(f"\n💾 Creating backup of original files...")
    backup_dir = Path('backup_env_original')
    backup_dir.mkdir(exist_ok=True)
    
    for file_key, file_path in env_files_paths.items():
        if file_path.exists():
            backup_path = backup_dir / f"{file_key}.backup"
            import shutil
            shutil.copy2(file_path, backup_path)
            print(f"✅ Backed up {file_path} to {backup_path}")
    
    print("\n" + "=" * 70)
    print("🎯 MERGE COMPLETED")
    print("=" * 70)
    print(f"📁 Merged file: {merged_file}")
    print(f"💾 Backups: {backup_dir}/")
    print(f"📊 Variables: {len(all_vars)} total, {len(conflict_resolutions)} conflicts resolved")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)