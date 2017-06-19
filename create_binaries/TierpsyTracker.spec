# -*- mode: python -*-
#hidden imports needed for tierpsy, maybe there is a better way to call this...
import tierpsy.analysis
base_name = os.path.dirname(tierpsy.analysis.__file__)
analysis_steps = [x for x in os.listdir(base_name) if os.path.exists(os.path.join(base_name, x, '__init__.py'))]
hidden_tierspy = ['tierpsy.analysis.' + x for x in analysis_steps]
print(hidden_tierspy)

import os
import sys
from PyInstaller.compat import is_win, is_darwin, is_linux

import tierpsy
import open_worm_analysis_toolbox
from tierpsy.helper.misc import FFMPEG_CMD, FFPROBE_CMD
from tierpsy.gui import SelectApp

#get TierpsyTracker main path
SRC_SCRIPT_PATH = SelectApp.__file__

DST_BUILD=os.path.abspath('.')
CREATE_CONSOLE= is_win #make a separated console only in windows. I have to do this due to a problem with pyinstaller

DEBUG = False

#get additional files
#openworm additional files
open_worm_path = os.path.dirname(open_worm_analysis_toolbox.__file__)

ow_feat = os.path.join('features', 'feature_metadata', 'features_list.csv')
ow_feat_src = os.path.join(open_worm_path, ow_feat)
ow_feat_dst = os.path.join('open_worm_analysis_toolbox', ow_feat)

ow_eigen = os.path.join('features', 'master_eigen_worms_N2.mat')
ow_eigen_src = os.path.join(open_worm_path, ow_eigen)
ow_eigen_dst = os.path.join('open_worm_analysis_toolbox', ow_eigen)

#add ffmpeg and ffprobe
ffmpeg_src = FFMPEG_CMD
ffmpeg_dst = os.path.join('extras', os.path.basename(FFMPEG_CMD))
ffprobe_src = FFPROBE_CMD
ffprobe_dst = os.path.join('extras', os.path.basename(FFPROBE_CMD))

#add prev compiled binary (they should have been ran before)
proccess_bin_dst = 'ProcessWorker'
if is_win:
  proccess_bin_dst += '.exe'
proccess_bin_src = os.path.join(DST_BUILD, 'dist', 'ProcessWorker', proccess_bin_dst)

#create added files
added_datas = [(ow_feat_dst, ow_feat_src, 'DATA'),
        (ow_eigen_dst, ow_eigen_src, 'DATA'),
        (proccess_bin_dst, proccess_bin_src, 'DATA'),
        (ffmpeg_dst, ffmpeg_src, 'DATA'),
        (ffprobe_dst, ffprobe_src, 'DATA')]

#I add the file separator at the end, it makes my life easier later on
tierpsy_path = os.path.dirname(tierpsy.__file__)
tierpsy_path += os.sep

#add all the files in extras
for (dirpath, dirnames, filenames) in os.walk(os.path.join(tierpsy_path, 'extras')):
  for fname in filenames:
    if not fname.startswith('.'):
      fname_src = os.path.join(dirpath, fname)
      fname_dst = fname_src.replace(tierpsy_path, '')
      added_datas.append((fname_dst, fname_src, 'DATA'))

#copy additional dll in windows
if is_win:
  import glob
  conda_bin = os.path.join(os.path.dirname(sys.executable), 'Library', 'bin')
  libopenh264_src = glob.glob(os.path.join(conda_bin, 'openh264*.dll'))
  libopencv_ffmpeg_src = glob.glob(os.path.join(conda_bin, 'opencv_ffmpeg*.dll'))
  
  for src in libopenh264_src + libopencv_ffmpeg_src:
    dst = os.path.basename(src)
    added_datas.append((dst, src, 'DATA'))
else:
  #copy some missing files from the library (at least in anaconda on OSX)
  for dst in ['libmkl_avx2.dylib', 'libmkl_mc.dylib']:
    src = os.path.realpath(os.path.join(os.path.dirname(sys.executable), '..', 'lib', dst))
    
    if os.path.exists(src):
      added_datas.append((dst, src, 'DATA'))
      print('<>><>>>>>>>>>>', dst)

    #THIS LIBRARY IS PROBLEMATIC BECAUSE THERE ARE MANY VERSIONS IN THE SYSTEM I HAVE TO IMPORT IT MANUALLY, BUT THIS COULD BREAK IN THE FUTURE
    

block_cipher = None
a = Analysis([SRC_SCRIPT_PATH],
             pathex=[DST_BUILD],
             binaries=None,
             datas = None,
             hiddenimports=['h5py.defs', 'h5py.utils', 'h5py.h5ac', 'h5py._proxy',
             'cython', 'sklearn', 'sklearn.neighbors.typedefs', 'pywt._extensions._cwt'] + hidden_tierspy,
             hookspath=[],
             runtime_hooks=[],
             excludes=['PyQt4', 'PyQt4.QtCore', 'PyQt4.QtGui'],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
#i was having problems with adding datas using Analysis, i decided to add them directly to a.datas

a.datas += added_datas
if is_darwin:
  a.binaries.append(('libfreetype.6.dylib', '/usr/local/opt/freetype/lib/libfreetype.6.dylib', 'BINARY'))
print([x for x in a.binaries if 'libfreetype' in x[0]])


pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)


if not DEBUG:

  exe = EXE(pyz,
            a.scripts,
            a.binaries,
            a.zipfiles,
            a.datas,
            name='TierpsyTracker',
            debug=False,
            strip=False,
            upx=True,
            console=CREATE_CONSOLE )

  if is_darwin:

    app = BUNDLE(exe,
                 name='TierpsyTracker.app',
                 icon=None,
                 bundle_identifier=None,
                 info_plist={
                  'CFBundleShortVersionString' : tierpsy.__version__,
                  'NSHighResolutionCapable': 'True'
                  }
                )

else:
  print('DEGUG')
  #do not create a single file if is debug
  exe = EXE(pyz,
            a.scripts,
            exclude_binaries=True,
            name='TierpsyTracker',
            debug=False,
            strip=False,
            upx=True,
            console=True )

  coll = COLLECT(exe,
                 a.binaries,
                 a.zipfiles,
                 a.datas,
                 strip=False,
                 upx=True,
                 name='TierpsyTracker')
