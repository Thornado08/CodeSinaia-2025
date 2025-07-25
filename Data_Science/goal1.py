import math

def calculate_p(px, py, pz):    #This function calculates the momentum of a particle given its components.
    return math.sqrt(px**2 + py**2 + pz**2)        #uses the formula for p

def calculate_pT (px, py):    #This function calculates the transverse momentum of a particle given its x and y components.    
    return math.sqrt(px**2 + py**2)  

def calculate_pseudorapidity(px, py, pz):               #pseudorapidity is the n with a long end
    return math.log((calculate_p(px, py, pz) + pz) /(calculate_p(px, py, pz) - pz))/2

def calculate_azimuthal_angle(px, py):      #solve if you finish early
    return math.atan(px/py)

def check_type (pdg):      #this function checks the type of particle based on the pdg code
    if abs(pdg) == 211:
        if(pdg == -211):
            return 1
        else:
            return -1
    return 0


#TODO: Open the input file, read the first line to get event_id and num_particles,
#       then read the rest of the lines into lines_list as lists of strings.
# TODO: Loop through each particle in lines_list, convert values to float,
#       call the analysis/calculation functions, and print the results as shown.

with open("../_Data/output-Set0.txt", "r") as fin:
    line = fin.readline()
    event_id_str, num_particles_str = line.split()

    event_id = int(event_id_str)
    num_particles = int(num_particles_str)

    print("event id is", event_id, "and there are", num_particles, "particles")  
    print("\n")     #print to show the events id and no of particles in the event

    for line_number, line in enumerate(fin, start=1):  # start=1 makes it 1-based
        px_str, py_str, pz_str, pdg_str = line.split()
        px = float(px_str)
        py = float(py_str)
        pz = float(pz_str)
        pdg = int(pdg_str)

        print(f"for particle {line_number} \n")

        if(check_type(pdg) == 1): print("this is a positive pion")
        if(check_type(pdg) == -1): print("this is a negative pion")
        if(check_type(pdg) == 0): print("this is not a pion")

        print(f"pseudorapidity = {calculate_pseudorapidity(px, py, pz)}")
        print(f"pT = {calculate_pT(px, py)}")
        print(f"azimuthal angle is {calculate_azimuthal_angle(px, py)} \n")
