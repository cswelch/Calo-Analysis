import numpy as np

# This is where the preliminary calo analysis code goes. Some representative output files from the simulation, including GDML angle data from photon impacts in the calo
# should be placed in this folder. The calo data is then analyzed via various methods below.

# Methods for converting GDML angles to (theta, phi) to be more easily interpreted and displayed.
def convert_to_spherical(coords):
    '''
        Converts a 3-Vector to spherical coordinates
    '''
    # print(coords)
    return [
        np.linalg.norm(coords)**2,
        np.arctan2(np.sqrt(coords[0]*coords[0] + coords[1]*coords[1]), coords[2]),
        np.arctan2(coords[1], coords[0])
    ]

def euler_to_thetaPhi(euler, degrees=True):
    '''
        Convert the Euler angles in the GDML file into a (theta,phi) pair for ploting
    '''
    from scipy.spatial.transform import Rotation as Rot
    roti = Rot.from_euler("xyz", euler, degrees=degrees)
    # print(roti)
    matrix = roti.as_matrix()
    out = np.matmul(matrix, [0,0,1])
    # print(out)
    # theta = np.arcsin()
    # print(matrix)
    angles = convert_to_spherical(out)[1:]
    # print(angles)
    return angles

def get_angles_from_gdml(infile, key='<rotation name="sipm_enclosure_'):
    angles = {}
    with open(infile, 'r') as f:
        for line in f:
            if key in line:
                # print(line)
                sipm = int(line.split(key)[1].split("_")[0])
                x = float(line.split('x="')[1].split('"')[0])
                y = float(line.split('y="')[1].split('"')[0])
                z = float(line.split('z="')[1].split('"')[0])
                # print(x,y,z)
                angles[sipm] = (-x,-y,-z)
    return angles


#TODO
# plot a 2d histogram of energy deposited in each SIPM "pixel" in the calorimeter.
def calo_edep_plot():
    return