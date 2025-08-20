"""
Migration helper for updating existing logging calls to use the new centralized system.

This module provides utilities to help migrate from the old logging patterns
to the new centralized logging system.
"""

import re
import ast
from typing import List, Dict, Any, Optional
from pathlib import Path


class LoggingMigrationHelper:
    """Helper class for migrating logging calls."""
    
    def __init__(self):
        self.old_patterns = [
            r'logging\.(info|debug|warning|error|critical)\s*\(',
            r'logger\.(info|debug|warning|error|critical)\s*\(',
        ]
        
        self.new_imports = [
            'from logging_utils import get_logger, log_info, log_debug, log_warning, log_error, log_critical',
            'from logging_utils import setup_logging',
        ]
    
    def find_logging_calls(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Find all logging calls in a file.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            List of dictionaries containing logging call information
        """
        calls = []
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse the file
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.Call):
                    if self._is_logging_call(node):
                        calls.append({
                            'line': node.lineno,
                            'col': node.col_offset,
                            'func': self._get_function_name(node),
                            'args': self._get_call_args(node),
                            'full_call': ast.unparse(node)
                        })
        
        except Exception as e:
            print(f"Error analyzing {file_path}: {e}")
        
        return calls
    
    def _is_logging_call(self, node: ast.Call) -> bool:
        """Check if a call node is a logging call."""
        if isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                return node.func.value.id in ['logging', 'logger']
            elif isinstance(node.func.value, ast.Attribute):
                return node.func.value.attr in ['logging', 'logger']
        return False
    
    def _get_function_name(self, node: ast.Call) -> str:
        """Get the function name from a call node."""
        if isinstance(node.func, ast.Attribute):
            return node.func.attr
        return "unknown"
    
    def _get_call_args(self, node: ast.Call) -> List[str]:
        """Get the arguments from a call node."""
        args = []
        for arg in node.args:
            if isinstance(arg, ast.Constant):
                args.append(repr(arg.value))
            else:
                args.append(ast.unparse(arg))
        return args
    
    def generate_migration_suggestions(self, file_path: str) -> str:
        """
        Generate migration suggestions for a file.
        
        Args:
            file_path: Path to the file to analyze
            
        Returns:
            String containing migration suggestions
        """
        calls = self.find_logging_calls(file_path)
        
        if not calls:
            return f"No logging calls found in {file_path}"
        
        suggestions = [f"# Migration suggestions for {file_path}"]
        suggestions.append("")
        
        # Group by function type
        by_function = {}
        for call in calls:
            func = call['func']
            if func not in by_function:
                by_function[func] = []
            by_function[func].append(call)
        
        for func, func_calls in by_function.items():
            suggestions.append(f"## {func.upper()} calls:")
            for call in func_calls:
                suggestions.append(f"# Line {call['line']}: {call['full_call']}")
                
                # Generate replacement
                if len(call['args']) >= 1:
                    message = call['args'][0]
                    replacement = f"log_{func}({message})"
                    suggestions.append(f"# Replace with: {replacement}")
                suggestions.append("")
        
        return "\n".join(suggestions)
    
    def create_migration_script(self, directory: str, output_file: str = "migration_suggestions.txt"):
        """
        Create a migration script for all Python files in a directory.
        
        Args:
            directory: Directory to scan
            output_file: Output file for suggestions
        """
        suggestions = ["# Logging Migration Suggestions", ""]
        
        for py_file in Path(directory).rglob("*.py"):
            if "logging_utils" not in str(py_file):
                file_suggestions = self.generate_migration_suggestions(str(py_file))
                suggestions.append(file_suggestions)
                suggestions.append("-" * 80)
                suggestions.append("")
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(suggestions))
        
        print(f"Migration suggestions written to {output_file}")


def quick_migrate_file(file_path: str) -> str:
    """
    Quick migration function for a single file.
    
    Args:
        file_path: Path to the file to migrate
        
    Returns:
        Migrated content as string
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add import if not present
        if 'from logging_utils import' not in content:
            import_line = 'from logging_utils import get_logger, log_info, log_debug, log_warning, log_error, log_critical\n'
            content = import_line + content
        
        # Replace logging calls
        replacements = [
            (r'logging\.info\s*\(', 'log_info('),
            (r'logging\.debug\s*\(', 'log_debug('),
            (r'logging\.warning\s*\(', 'log_warning('),
            (r'logging\.error\s*\(', 'log_error('),
            (r'logging\.critical\s*\(', 'log_critical('),
            (r'logger\.info\s*\(', 'log_info('),
            (r'logger\.debug\s*\(', 'log_debug('),
            (r'logger\.warning\s*\(', 'log_warning('),
            (r'logger\.error\s*\(', 'log_error('),
            (r'logger\.critical\s*\(', 'log_critical('),
        ]
        
        for pattern, replacement in replacements:
            content = re.sub(pattern, replacement, content)
        
        return content
    
    except Exception as e:
        return f"Error migrating {file_path}: {e}"


if __name__ == "__main__":
    # Example usage
    helper = LoggingMigrationHelper()
    
    # Generate migration suggestions for the entire project
    helper.create_migration_script(".")
    
    print("Migration helper ready!")
    print("Use quick_migrate_file() for individual files")
    print("Use LoggingMigrationHelper() for detailed analysis") 