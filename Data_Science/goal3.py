import math
import time
import matplotlib.pyplot as plt
import re
from pathlib import Path
from multiprocessing import Pool, cpu_count
import numpy as np
from scipy.stats import f_oneway

data_folder = Path("../_Data")
pattern = re.compile(r".*(?:[1-9]|10)\.txt$")
files = sorted([f for f in data_folder.glob("*.txt") if pattern.match(f.name)])

threshold = 0.05
batch_size = 1000

def check_type(pdg_code):
    if abs(pdg_code) == 211:
        return 1 if pdg_code > 0 else -1
    return 0

def poisson_distribution(n):
    return math.sqrt(n)

def difference(no_1, no_2):
    return abs(no_1 - no_2)

def combined_uncertainty(no_1, no_2):
    return math.sqrt(no_1 + no_2)

def significance(no_1, no_2, comb_uncertainty):
    return abs(no_1 - no_2) / comb_uncertainty if comb_uncertainty != 0 else 0

def process_file(filepath):
    count = 0
    pos = 0
    neg = 0
    total_events = 0

    pos_per_batch = []
    neg_per_batch = []
    batch_ind = []

    start_time = time.time()

    with open(filepath, "r") as fin:
        batch_pos = 0
        batch_neg = 0
        events_in_batch = 0

        while True:
            header = fin.readline()
            if not header:
                break

            try:
                event_id, num_particles = map(int, header.strip().split())
            except ValueError:
                continue

            event_pos = 0
            event_neg = 0

            for _ in range(num_particles):
                particle_line = fin.readline()
                if not particle_line:
                    break

                try:
                    px, py, pz, pdg = particle_line.strip().split()
                    pdg = int(pdg)
                except ValueError:
                    continue

                ispion = check_type(pdg)
                if ispion == 1:
                    event_pos += 1
                elif ispion == -1:
                    event_neg += 1

            batch_pos += event_pos
            batch_neg += event_neg
            pos += event_pos
            neg += event_neg
            total_events += 1
            events_in_batch += 1

            if events_in_batch == batch_size:
                count += 1
                pos_per_batch.append(batch_pos)
                neg_per_batch.append(batch_neg)
                batch_ind.append((count - 1) * batch_size)
                batch_pos = 0
                batch_neg = 0
                events_in_batch = 0

        if events_in_batch > 0:
            count += 1
            pos_per_batch.append(batch_pos)
            neg_per_batch.append(batch_neg)
            batch_ind.append((count - 1) * batch_size)

    avg_pos = pos / total_events if total_events else 0
    avg_neg = neg / total_events if total_events else 0
    poisson_pos = poisson_distribution(pos)
    poisson_neg = poisson_distribution(neg)
    diff = difference(pos, neg)
    comb_unc = combined_uncertainty(pos, neg)
    sig = significance(pos, neg, comb_unc)

    end_time = time.time()
    elapsed = end_time - start_time

    result = {
        "filename": filepath.name,
        "avg_pos": avg_pos,
        "avg_neg": avg_neg,
        "poisson_pos": poisson_pos,
        "poisson_neg": poisson_neg,
        "diff": diff,
        "combined_uncertainty": comb_unc,
        "significance": sig,
        "is_significant": sig > threshold,
        "pos_per_batch": pos_per_batch,
        "neg_per_batch": neg_per_batch,
        "batch_ind": batch_ind,
        "runtime": elapsed,
        "total_events": total_events
    }

    return result

if __name__ == "__main__":
    # Process files in parallel
    with Pool(processes=cpu_count()) as pool:
        results = pool.map(process_file, files)

    runtimes = []
    file_labels = []

    for res in results:
        # Prepare data
        pos_per_event = [p / batch_size for p in res["pos_per_batch"]]
        neg_per_event = [n / batch_size for n in res["neg_per_batch"]]
        batch_index = res["batch_ind"]
        label = res["filename"]

        # Run ANOVA between the two groups (pos vs neg per batch)
        f_stat, p_val = f_oneway(pos_per_event, neg_per_event)

        # Plot ANOVA-style line chart
        plt.figure(figsize=(10, 6))
        plt.plot(batch_index, pos_per_event, marker='o', linestyle='-', label="Positive pions")
        plt.plot(batch_index, neg_per_event, marker='s', linestyle='--', label="Negative pions")

        plt.title(f"{label}\nANOVA: F = {f_stat:.2f}, p = {p_val:.3e}")
        plt.xlabel("Event Number (Batch Start)")
        plt.ylabel("Average Pions per Event")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.legend()
        plt.tight_layout()
        plt.show()

        # Save runtime info
        runtimes.append(res["runtime"])
        file_labels.append(label)

    # Final runtime comparison plot
    plt.figure(figsize=(10, 5))
    bars = plt.bar(file_labels, runtimes, color='skyblue')
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, yval + 0.01, f"{yval:.2f}s", ha='center', va='bottom')
    plt.title("Runtime per File")
    plt.ylabel("Time (seconds)")
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.show()
