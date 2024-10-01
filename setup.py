from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': [], 'excludes': [], 'includes': ['guizero']}

base = 'gui'

executables = [
    Executable('HoneyFetch.py', base=base)
]

setup(name='HoneyFetch',
      version = '1.0',
      description = 'Diagnostic tool for Sonic the Fighters on RPCS3.',
      options = {'build_exe': build_options},
      executables = executables)
