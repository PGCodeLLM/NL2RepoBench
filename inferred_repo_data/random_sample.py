import json
import random

# Input and output file names
input_filename = "repo_lines.json"
output_filename = "sampled_30_nl2r.json"

# 1. Read the raw data from the JSON file
with open(input_filename, "r", encoding="utf-8") as infile:
    raw_data = json.load(infile)

# 2. Initialize our strict data buckets
easy_tier = []
medium_tier = []
hard_tier = []

# 3. Filter strictly based on your criteria
for item in raw_data:
    loc = item.get("lines_of_code", 0)
    difficulty = item.get("difficulty", "")
    
    # Easy: < 1.5k lines
    if difficulty == "Easy" and loc < 1500:
        easy_tier.append(item)
    # Medium: 1.5k - 4k lines
    elif difficulty == "Medium" and 1500 <= loc <= 4000:
        medium_tier.append(item)
    # Hard: > 4k lines
    elif difficulty == "Hard" and loc > 4000:
        hard_tier.append(item)

# 4. Randomly sample exactly 10 from each valid bucket
sampled_results = {
    "Easy": random.sample(easy_tier, min(10, len(easy_tier))),
    "Medium": random.sample(medium_tier, min(10, len(medium_tier))),
    "Hard": random.sample(hard_tier, min(10, len(hard_tier)))
}

# 5. Dump the sampled results directly into the destination file
with open(output_filename, "w", encoding="utf-8") as outfile:
    json.dump(sampled_results, outfile, indent=4, ensure_ascii=False)

print(f"Done! Successfully read '{input_filename}' and dumped results to '{output_filename}'.")