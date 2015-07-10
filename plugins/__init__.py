import os,glob
glob_names = os.path.dirname(__file__) + "/handle*.py"
import_files = glob.glob(glob_names)

__all__ = []
for f in import_files:

  filename = os.path.basename(f).split(".")[0]
  if filename != "__init__":
    __all__.append(filename)
