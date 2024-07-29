import random
import Files.scripts.assets as assets
from Files.scripts.Data.Battlers import BattlersType

def calculate_spawn_probabilities(battlers):
    # Calculate the sum of base stats for each battler
    stats_sums = {name: sum(stats["BaseStat"].values()) for name, stats in battlers.items()}
    
    # Calculate the inverted sum to make battlers with lower stats more common
    max_stats = max(stats_sums.values())
    inverted_sums = {name: max_stats - stats_sum + 1 for name, stats_sum in stats_sums.items()}  # +1 to avoid zero probability
    
    # Calculate spawn weights based on inverted sums and spawn values
    weighted_sums = {name: inverted_sum * battlers[name]["Spawn"] for name, inverted_sum in inverted_sums.items()}
    
    # Calculate total of weighted sums
    total_weighted_sum = sum(weighted_sums.values())
    
    # Calculate spawn probabilities
    probabilities = {name: weighted_sum / total_weighted_sum for name, weighted_sum in weighted_sums.items()}
    
    return probabilities

# Calculate spawn probabilities
spawn_probabilities = calculate_spawn_probabilities(BattlersType)

# Example of generating a spawn list based on probabilities
def generate_spawn_list(probabilities, num_spawns=1000):
    battler_names = list(probabilities.keys())
    battler_probabilities = list(probabilities.values())
    
    spawn_list = random.choices(battler_names, battler_probabilities, k=num_spawns)
    return spawn_list


spawn_list = generate_spawn_list(spawn_probabilities)