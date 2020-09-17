#! /usr/bin/env python3

import h5py
import os
from pathlib import Path
import platform
import shutil
import subprocess
import tarfile
from tempfile import TemporaryDirectory
import urllib.request


def package_lib():
    # Copy the binaries
    if platform.system() == 'Linux':
        lib_location = '.libs'
        lib_extension = '.so'
        lib_pattern = 'libhdf5-*'
    else:
        lib_location = '.dylibs'
        lib_extension = '.dylib'
        lib_pattern = 'libhdf5.*.dylib'

    libdir = Path(h5py.__file__).parent / lib_location
    if not Path('lib').exists():
        shutil.copytree(libdir, 'lib')
        lib = Path('lib').glob(lib_pattern).__next__()
        Path('lib/libhdf5' + lib_extension).symlink_to(lib.name)

        if platform.system() == 'Darwin':
            # Patch the library install path
            cmd = f'install_name_tool -id @loader_path/../lib/{lib.name} lib/{lib.name}'
            subprocess.run(cmd, shell=True, check=True)

    # Get the C headers
    if not Path('include').exists():
        version = h5py.version.hdf5_version
        shortver, _ = version.rsplit('.', 1)
        archive = f'hdf5-{version}.tar.gz'
        baseurl = 'https://www.hdfgroup.org/ftp/HDF5/releases/'
        url = baseurl + f'hdf5-{shortver}/hdf5-{version}/src/' + archive

        incdir = Path('include').resolve()
        with TemporaryDirectory() as tmpdir:
            os.chdir(tmpdir)
            urllib.request.urlretrieve(url, archive)

            with tarfile.open(archive, 'r:gz') as tar:
                tar.extractall()

            os.chdir(f'hdf5-{version}')
            subprocess.run('./configure', shell=True, capture_output=True)

            includes = []
            with open('src/Makefile') as f:
                for line in f:
                    if not includes:
                        if line.startswith('include_HEADERS ='):
                            includes += line.split()[2:-1]
                    else:
                        tmp = line.split()
                        if tmp[-1] == '\\':
                            includes += tmp[:-1]
                        else:
                            includes += tmp
                            break

            incdir.mkdir(exist_ok=True)
            for include in includes:
                shutil.copy('src/' + include, incdir)
        os.chdir(incdir.parent)

    # Package the lib
    version = h5py.version.hdf5_version
    archive = f'libhdf5-{version}.tgz'
    with tarfile.open(archive, 'w:gz') as tar:
        tar.add('include')
        tar.add('lib')


if __name__ == '__main__':
    package_lib()
