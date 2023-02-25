import argparse
from multiprocessing import Pool
import glob
import openmc.data
import os
import warnings

# Add parser arguments for temperature input
parser = argparse.ArgumentParser(description='Process neutron data for a given temperature')
parser.add_argument('--temperature', type=int, nargs='+', default=[294], help='Temperature(s) in K')
args = parser.parse_args()

neutron_files = sorted(glob.glob('*.dat'))

library = openmc.data.DataLibrary()

def process_neutron(path, temperatures):
    nuclide = os.path.splitext(os.path.basename(path))[0]
    print(f'Processing {nuclide} ...')
    data = openmc.data.IncidentNeutron.from_njoy(path, temperatures=temperatures)

    h5_file = f'{data.name}.h5'
    print(f'Writing {h5_file} ...')
    data.export_to_hdf5(h5_file, 'w', libver = 'latest')

def process_thermal(path_neutron, path_thermal):
    thermal_name = os.path.splitext(os.path.basename(path_thermal))[0]
    print(f'Processing: {thermal_name}')
    try:
        with warnings.catch_warnings():
            warnings.simplefilter('ignore', UserWarning)
            data = openmc.data.ThermalScattering.from_njoy(
                path_neutron, path_thermal
            )
    except Exception as e:
        print(path_neutron, path_thermal, e)
        raise
    h5_file = f'{data.name}.h5'
    print(f'Writing {h5_file} ...')
    data.export_to_hdf5(h5_file, 'w', libver = 'latest')

with Pool() as pool:
    results = []
    for filename in neutron_files:
        func_args = (filename, args.temperature)
        r = pool.apply_async(process_neutron, func_args)
        results.append(r)

    # Add pairs of neutron and thermal data to be processed concurrently
    thermal_data = [
        ('H1.dat', 'HinH2O.dat'),
        ('H1.dat', 'HinZrH.dat'),
        ('Zr90.dat', 'ZrinZrH.dat')
    ]
    for thermal_pair in thermal_data:
        func_args = (thermal_pair[0], thermal_pair[1])
        r = pool.apply_async(process_thermal, func_args)
        results.append(r)

    for r in results:
        r.wait()

# Register with library
for p in sorted(glob.glob('*.h5')):
    library.register_file(p)

# Write cross_sections.xml
library.export_to_xml('cross_sections.xml')
