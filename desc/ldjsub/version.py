# version.py
#
# David Adams
# October 2022

import desc.ldjsub

def version():
  return desc.ldjsub.__version__

def main_version():
  print(desc.ldjsub.version())
