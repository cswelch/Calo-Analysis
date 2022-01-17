from operator import indexOf
import numpy as np
from matplotlib import pyplot as plt

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
        Convert the Euler angles in the GDML file into a (theta,phi) pair for plotting
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

#TODO: Use RegEx to get IDs of sipms, can use ID to find edep branch from root file
def get_angles_from_gdml(infile, key='<rotation name="HEX'):
    angles = {}
    with open(infile, 'r') as f:
        for line in f: 
            if key in line:
                # print(line)
                sipm = int(line.split("0_")[1].split("_")[0])
                x = float(line.split('x="')[1].split('"')[0])
                y = float(line.split('y="')[1].split('"')[0])
                z = float(line.split('z="')[1].split('"')[0])
                # print(x,y,z)
                angles[sipm] = (-x,-y,-z)
    return angles


# plot a 2d histogram of energy deposited in each SIPM "pixel" in the calorimeter.
def calo_edep_plot():
    #Open file
    # PiEfile = r.TFile("pienux_out_stripped.root")
    # PiEtree = PiEfile.Get("atar")
    # # print([x.GetName() for x in tree.GetListOfBranches()])
    # # print("\n")

    # (max_Es_DIF, gap_times_DIF) = event_visualization(PiEtree, 0, False, False, 100)
    # (max_Es_DAR, gap_times_DAR) = event_visualization(PiEtree, 1, False, False, 100)

    # compare_max_edep(max_Es_DIF, max_Es_DAR, 20)
    # compare_gap_times(gap_times_DIF, gap_times_DAR, 20)

    angles = get_angles_from_gdml("calo_only_PEN.gdml")
    angles_list = list(angles.values())
    angles_thetaPhi = [euler_to_thetaPhi(angles_list[i]) for i in range(len(angles))]
    print(len(angles_thetaPhi))
    plt.hist2d([ang[0] for ang in angles_thetaPhi], [ang[1] for ang in angles_thetaPhi], bins = 50)
    plt.xlabel("Theta (rad)")
    plt.ylabel("Phi (rad)")
    plt.title("Energy Deposited in Calorimeter SiPMs by Theta vs. Phi")
    plt.colorbar(orientation="vertical")
    plt.show()
    return

calo_edep_plot()