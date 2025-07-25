import math
import matplotlib.pyplot as plt
import numpy as np
import time

start_time = time.time()

threshold = 0.05

# Returns 1 for positive pion (211), -1 for negative pion (-211), 0 otherwise
def check_type(pdg_code):
    if abs(pdg_code) == 211:
        if(pdg_code == 211):
            return 1
        else:
            return -1
    return 0

# Returns the Poisson uncertainty for a given average
def poisson_distribution(average):
    return math.sqrt(average)

# Returns the absolute difference between two numbers
def difference(no_1, no_2):
    return abs(no_1 - no_2)

# Returns the combined uncertainty for two numbers
def combined_uncertainty(no_1, no_2):
    return math.sqrt(no_1 + no_2)

# Returns the significance of the difference
def significance(no_1, no_2, comb_uncertainty):
    return abs(no_1 - no_2) / comb_uncertainty

# TODO: Open the input file, read the first line to get event_id and num_particles,
#       then read the rest of the lines into lines_list as lists of strings.
#       Handle FileNotFoundError and IOError with appropriate messages--> handle file errors.

# TODO: Loop through each particle in lines_list, convert values to float,
#       use check_type to count positive and negative pions per event.

# TODO: You may use batching (e.g., sum per 1000 events) or sampling (store per-event counts).
#       Batching is recommended for large files to reduce memory usage.
#       Sampling (storing per-event counts) is useful if you want to analyze or plot per-event data.

# TODO: After processing, print the total number of positive and negative pions,
#       their averages per event, Poisson uncertainties, the difference, combined uncertainty, and significance.
#       Print whether the significance is above the threshold.

# TODO: Plot a single graph showing the number of positive and negative pions in each batch of 1000 events.
#       X-axis: event number (0, 1000, 2000, ...)
#       Y-axis: number of pions in each batch of 1000 events
#       The plot should have two lines: one for positive pions, one for negative pions.

# Example expected output (printed):
# In 500000 total events, we had 9238697 positive particles and 9225784 negative particles.
# there s an average of  18.477394 particles(positive pions)
# there s an average of  18.451568 anti-particles(negative pions)
# the poisson distribution for the positive pions is 3039.52 ...
# the poisson distribution for the negative(antiparticle) pions is 3037.39 ...
# there are  12913  more particles then antiparticles
# the combined uncertainty of the total amount of particles and antiparticles is  4297.03 ...
# the significance is  3.00 ...
# the significance is very large compared to the threshold

# Example expected plot:
# A line plot with two lines (positive and negative pions per 1000 events), x-axis labeled "Event number", y-axis labeled "Number of pions in 1000 events".

batch = 10000  # number of events to process
count = 0
pos = 0
neg = 0
total_events = 0
events_in_batch = 0

pos_per_batch = []
neg_per_batch = []
batch_ind = []

with open("../_Data/output-Set1.txt") as fin:
    while True:
        batch_pos = 0
        batch_neg = 0
        events_in_batch = 0

        for _ in range(batch):
            line = fin.readline()
            if not line:
                break

            event_id, num_particles = map(int, line.split())

            for _ in range(num_particles):
                px, py, pz, pdg = fin.readline().split()
                px, py, pz, pdg = *map(float, (px, py, pz)), int(pdg)

                ispion = check_type(pdg)
                if ispion == 1:
                    batch_pos += 1
                elif ispion == -1:
                    batch_neg += 1
                
            events_in_batch += 1
            
        if events_in_batch == 0:
            break
        
        count += 1
        pos += batch_pos
        neg += batch_neg
        total_events += events_in_batch

        pos_per_batch.append(batch_pos)
        neg_per_batch.append(batch_neg)
        batch_ind.append((count-1) * batch)


avg_pos = pos / total_events
avg_neg = neg / total_events

poisson_pos = poisson_distribution(pos)
poisson_neg = poisson_distribution(neg)

diff = difference(pos, neg)
comb_uncertainty = combined_uncertainty(pos, neg)
sig = significance(pos, neg, comb_uncertainty)

print(f"In {total_events} total events, we had {pos} positive pions and {neg} negative pions.")
print(f"Average positive pions per event: {avg_pos:.8f}")
print(f"Average negative pions per event: {avg_neg:.8f}")
print(f"Poisson uncertainty for positive pions: {poisson_pos:.8f}")
print(f"Poisson uncertainty for negative pions: {poisson_neg:.8f}")
print(f"There are {diff} more positive than negative pions.")
print(f"Combined uncertainty: {comb_uncertainty:.8f}")
print(f"Significance: {sig:.8f}")
if sig > threshold:
    print(f"The significance is above the threshold of {threshold}.")
else:
    print(f"The significance is below the threshold of {threshold}.")

plt.figure(figsize=(10,6))
plt.plot(batch_ind, pos_per_batch, label="Positive pions per 1000 events")
plt.plot(batch_ind, neg_per_batch, label="Negative pions per 1000 events")
plt.xlabel("Event Number")
plt.ylabel("Number of Pions in Batch")
plt.title("Positive and Negative Pions per 1000 Events")
plt.legend()
plt.grid(True)
plt.show()

end_time = time.time()

elapsed_time = end_time - start_time

print(f"Runtime: {elapsed_time} seconds")

with open("batching_results.txt", "w") as f:
    for i in range(len(batch_ind)):
        f.write(f"{batch_ind[i]},{pos_per_batch[i]},{neg_per_batch[i]}\n")

with open("batching_runtime.txt", "w") as f:
    f.write(str(elapsed_time))
