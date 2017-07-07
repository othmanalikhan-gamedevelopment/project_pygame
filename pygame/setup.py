import os
import sys

from cx_Freeze import setup, Executable

PYTHON_INSTALL_DIR = os.path.join("C:\\Users", "OzAli", "Anaconda3")
os.environ['TCL_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tcl8.6')
os.environ['TK_LIBRARY'] = os.path.join(PYTHON_INSTALL_DIR, 'tcl', 'tk8.6')

base = None
if sys.platform == "win32":
    base = "Win32GUI"

buildOptions = dict(packages=["pygame"],
                    excludes=["tkinter",
                              "email",
                              "html",
                              "http",
                              "xml",
                              "xmlrpc",
                              "lib2to3",
                              "json",
                              "ctypes",
                              "multiprocessing",
                              "pydoc_data",
                              "urllib",
                              "distutils",
                              "logging",
                              "unittest",
                              "test"
                              ],
                    include_files=["README",
                                   "LICENSE",
                                   "Artwork/",
                                   "Extra/"],
                    build_exe="build")

executables = [
    Executable('exiled.py',
               targetName="exiled.exe",
               base=base)
]

setup(name='exiled',
      version='1.0',
      description='A platformer (grappling hook) game made using pygame',
      options=dict(build_exe=buildOptions),
      executables=executables
)

