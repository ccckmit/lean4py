"""API documentation generator for lean4py."""

import inspect
import sys


def generate_api_doc(output_file: str = 'API_REFERENCE.md') -> None:
    """Generate API reference from module docstrings."""
    modules = [
        'lean4py.logic',
        'lean4py.sets',
        'lean4py.algebra',
        'lean4py.nat',
        'lean4py.tactics',
        'lean4py.prover',
        'lean4py.number_theory',
        'lean4py.linear_algebra',
        'lean4py.real_analysis',
        'lean4py.probability',
        'lean4py.graph_theory',
        'lean4py.statistics',
        'lean4py.optimization',
        'lean4py.symbolic',
        'lean4py.pde',
        'lean4py.time_series',
    ]
    
    with open(output_file, 'w') as f:
        f.write('# lean4py API Reference\n\n')
        f.write('Generated automatically from docstrings.\n\n')
        
        for module_name in modules:
            try:
                __import__(module_name, fromlist=[''])
                module = sys.modules[module_name]
                f.write(f'## {module_name}\n\n')
                
                # Get all functions
                members = inspect.getmembers(module, inspect.isfunction)
                for name, func in sorted(members):
                    if name.startswith('_'):
                        continue
                    f.write(f'### {name}\n')
                    if func.__doc__:
                        f.write(f'{func.__doc__}\n\n')
                    else:
                        f.write('No docstring.\n\n')
            except ImportError as e:
                f.write(f'Error importing {module_name}: {e}\n\n')
    
    print(f'Generated {output_file}')


if __name__ == '__main__':
    generate_api_doc()
