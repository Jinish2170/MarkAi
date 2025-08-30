#!/usr/bin/env python3
"""
MarkAI Import Fixer - Automatically fixes common import issues

This script scans Python files in the MarkAI project and automatically
fixes common import problems.
"""

import os
from pathlib import Path
from typing import List, Dict


class ImportFixer:
    """Fixes common import issues in Python files"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.changes_made: Dict[str, List[str]] = {}
        
    def find_python_files(self) -> List[Path]:
        """Find all Python files in the project"""
        python_files = []
        
        # Skip certain directories
        skip_dirs = {'.git', '__pycache__', '.pytest_cache', 'venv', 'env', 'node_modules'}
        
        for root, dirs, files in os.walk(self.project_root):
            # Remove skip directories from dirs list
            dirs[:] = [d for d in dirs if d not in skip_dirs]
            
            for file in files:
                if file.endswith('.py'):
                    python_files.append(Path(root) / file)
        
        return python_files
    
    def analyze_file(self, file_path: Path) -> Dict[str, any]:
        """Analyze a Python file for import issues"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (IOError, OSError, UnicodeError) as e:
            return {'error': str(e)}
        
        lines = content.split('\n')
        
        analysis = {
            'has_markai_imports': False,
            'has_import_helper': False,
            'has_sys_path_modification': False,
            'relative_imports': [],
            'markai_imports': [],
            'issues': []
        }
        
        for i, line in enumerate(lines):
            stripped = line.strip()
            
            # Check for MarkAI module imports
            markai_modules = ['core.', 'memory.', 'plugins.', 'utils.', 'cli.', 'api.']
            for module in markai_modules:
                if f'from {module}' in stripped or f'import {module}' in stripped:
                    analysis['has_markai_imports'] = True
                    analysis['markai_imports'].append((i + 1, stripped))
            
            # Check for import helper usage
            if 'import_helper' in stripped and 'setup_project_imports' in stripped:
                analysis['has_import_helper'] = True
            
            # Check for sys.path modifications
            if 'sys.path' in stripped and ('insert' in stripped or 'append' in stripped):
                analysis['has_sys_path_modification'] = True
            
            # Check for relative imports
            if stripped.startswith('from .') or stripped.startswith('from ..'):
                analysis['relative_imports'].append((i + 1, stripped))
        
        # Identify issues
        if analysis['has_markai_imports'] and not analysis['has_import_helper']:
            analysis['issues'].append('Has MarkAI imports but no import helper')
        
        if analysis['relative_imports']:
            analysis['issues'].append('Uses relative imports')
        
        return analysis
    
    def fix_file(self, file_path: Path, analysis: Dict) -> bool:
        """Fix import issues in a file"""
        if not analysis['issues']:
            return False
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (IOError, OSError, UnicodeError) as e:
            print(f"❌ Error reading {file_path}: {e}")
            return False
        
        lines = content.split('\n')
        changes = []
        
        # Fix 1: Add import helper if needed
        if 'Has MarkAI imports but no import helper' in analysis['issues']:
            # Find the first MarkAI import line
            first_markai_import = None
            for line_num, line_content in analysis['markai_imports']:
                if first_markai_import is None:
                    first_markai_import = line_num - 1  # Convert to 0-based index
                    break
            
            if first_markai_import is not None:
                # Insert import helper before first MarkAI import
                import_helper_lines = [
                    "# Setup imports using the import helper",
                    "from utils.import_helper import setup_project_imports",
                    "setup_project_imports()",
                    ""
                ]
                
                for i, helper_line in enumerate(import_helper_lines):
                    lines.insert(first_markai_import + i, helper_line)
                
                changes.append("Added import helper setup")
        
        # Fix 2: Convert relative imports to absolute
        if analysis['relative_imports']:
            for line_num, line_content in analysis['relative_imports']:
                line_index = line_num - 1  # Convert to 0-based
                
                # Simple conversion from relative to absolute
                # This is a basic implementation - might need refinement
                if line_content.startswith('from .'):
                    # Try to determine the module path based on file location
                    relative_path = file_path.relative_to(self.project_root)
                    parent_module = '.'.join(relative_path.parent.parts)
                    
                    # Replace relative import with absolute
                    new_line = line_content.replace('from .', f'from {parent_module}.')
                    lines[line_index] = new_line
                    changes.append(f"Converted relative import on line {line_num}")
        
        if changes:
            # Write the fixed content back
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(lines))
                
                self.changes_made[str(file_path)] = changes
                return True
            except (IOError, OSError, UnicodeError) as e:
                print(f"❌ Error writing {file_path}: {e}")
                return False
        
        return False
    
    def run_fixes(self, dry_run: bool = False) -> Dict[str, any]:
        """Run import fixes on all Python files"""
        python_files = self.find_python_files()
        
        results = {
            'total_files': len(python_files),
            'files_with_issues': 0,
            'files_fixed': 0,
            'issues_found': {},
            'changes_made': {}
        }
        
        print(f"🔍 Scanning {len(python_files)} Python files...")
        
        for file_path in python_files:
            relative_path = file_path.relative_to(self.project_root)
            analysis = self.analyze_file(file_path)
            
            if 'error' in analysis:
                print(f"❌ Error analyzing {relative_path}: {analysis['error']}")
                continue
            
            if analysis['issues']:
                results['files_with_issues'] += 1
                results['issues_found'][str(relative_path)] = analysis['issues']
                
                print(f"\n📁 {relative_path}")
                for issue in analysis['issues']:
                    print(f"  ⚠️  {issue}")
                
                if not dry_run:
                    if self.fix_file(file_path, analysis):
                        results['files_fixed'] += 1
                        results['changes_made'][str(relative_path)] = self.changes_made[str(file_path)]
                        print("  ✅ Fixed!")
                        for change in self.changes_made[str(file_path)]:
                            print(f"    - {change}")
                    else:
                        print("  ❌ Could not fix automatically")
                else:
                    print("  🔧 Would fix in non-dry-run mode")
        
        return results


def main():
    """Main function"""
    project_root = Path(__file__).parent
    
    print("🚀 MarkAI Import Fixer")
    print("=" * 40)
    
    fixer = ImportFixer(project_root)
    
    # First run a dry run to see what would be fixed
    print("🔍 Running analysis (dry run)...")
    dry_results = fixer.run_fixes(dry_run=True)
    
    print("\n📊 Analysis Results:")
    print(f"  Total files scanned: {dry_results['total_files']}")
    print(f"  Files with issues: {dry_results['files_with_issues']}")
    
    if dry_results['files_with_issues'] > 0:
        print(f"\n⚠️  Found issues in {dry_results['files_with_issues']} files")
        
        response = input("Would you like to fix these issues? (y/n): ").lower().strip()
        
        if response in ['y', 'yes']:
            print("\n🔧 Applying fixes...")
            fix_results = fixer.run_fixes(dry_run=False)
            
            print(f"\n✅ Fixed {fix_results['files_fixed']} files")
            print("\n🎉 Import issues resolved!")
        else:
            print("🚫 No changes made. Run with fixes to apply changes.")
    else:
        print("🎉 No import issues found! Your project is already properly configured.")


if __name__ == "__main__":
    main()
