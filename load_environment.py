import os

def load_environment(file_path):
    with open(file_path) as f:
        for line in f:
            if line.strip() and not line.startswith("#"):
                key, value = line.strip().split("=", 1)
                os.environ[key] = value

# Načtení environmentálních proměnných z environment.txt
load_environment("environment.txt")