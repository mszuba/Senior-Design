import numpy as np

def phase_comp(p1,p2,p3,p4):
    """Compares phases from four arrays of FFT samples"""
    #-------currently only for 1 number arrary-----------

    wave_len = 0.122    # 122 mm @ 2.45 GHz
    a = 0.11            # Spacing between antennas (m)

    # Phase Differences
    diff_21 = p2-p1
    diff_31 = p3-p1
    diff_24 = p2-p4
    diff_34 = p3-p4

    # Angles with reference to antenna 1
    az_1= np.arctan2(diff_21,diff_31)*57.2958 # convert to degrees
    el_1_num = np.sqrt((np.square(diff_21))+np.square(diff_31))
    el_1_den = (2*np.pi*a) / wave_len
    el_1 = np.arccos((el_1_num/el_1_den))

    # Angles with reference to antenna 4
    az_2= np.arctan2(diff_24,diff_34)*57.2958   # convert to degrees
    el_2_num = np.sqrt((np.square(diff_24))+np.square(diff_34))
    el_2_den = (2*np.pi*a) / wave_len
    el_2 = np.arccos((el_2_num/el_2_den))

    # Print output for testing
    print('Az_1: {}     Az_2: {}'.format(az_1,az_2))
    print('El_1: {}     El_2: {}'.format(el_1,el_2))

def average_angles(az_angles_1,az_angles_2, el_angles_1, el_angles_2):
    """Averages the angles calculated"""
    n = 0
    az_sum = 0
    el_sum = 0
    while n < 200:
        az_sum = az_angles_1[n] + az_angles_2[n]
        el_sum = el_angles_1[n] + el_angles_2[n]
        n+=1
    az_avg = az_sum / 200
    el_avg = el_sum / 200

    # Print for testing
    print('Az_avg: ', str(az_avg))
    print('El_avg: ', str(el_avg))

    return(az_avg,el_avg)
