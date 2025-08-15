# Unittests and Integration Tests

This project contains Python modules and tests focused on unit testing and integration testing best practices. It is designed to be interpreted/compiled on Ubuntu 18.04 LTS using Python 3.7.

## Requirements

- All files must end with a new line.
- The first line of all Python files should be exactly `#!/usr/bin/env python3`.
- All code must follow the [pycodestyle](https://pycodestyle.readthedocs.io/en/latest/) style guide (version 2.5).
- All files must be executable.
- All modules, classes, and functions must have proper documentation strings. Documentation should be a real sentence explaining the purpose of the module, class, or method.
- All functions and coroutines must be type-annotated.

## Structure

- `test_utils.py`: Contains unit tests for utility functions using the `unittest` and `parameterized` libraries.
- `utils.py`: Utility functions to be tested.

## Documentation

To verify documentation, use the following commands:

- Module: `python3 -c 'print(__import__("my_module").__doc__)'`
- Class: `python3 -c 'print(__import__("my_module").MyClass.__doc__)'`
- Function: `python3 -c 'print(__import__("my_module").my_function.__doc__)'`
- Method: `python3 -c 'print(__import__("my_module").MyClass.my_function.__doc__)'`

## Testing

Tests are written using the `unittest` framework and `parameterized` for multiple test cases. Run tests with:

```bash
python3 -m unittest test_utils.py
```

## License

This project is for educational purposes.
