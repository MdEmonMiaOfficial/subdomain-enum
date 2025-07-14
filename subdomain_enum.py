import os
import subprocess

# ===== CONFIGURATION =====
domain = input("Enter the domain (e.g. example.com): ")
output_dir = f"./output/{domain}"
os.makedirs(output_dir, exist_ok=True)

# ===== TOOL PATHS =====
tools = {
    "assetfinder": "assetfinder",
    "subfinder": "subfinder",
    "amass": "amass",
    "gau": "gau"
}

# ===== RUN ENUMERATION TOOLS =====

def run_tool(name, command, output_file):
    print(f"[+] Running {name}...")
    with open(output_file, "w") as f:
        subprocess.run(command, shell=True, stdout=f, stderr=subprocess.DEVNULL)
    print(f"[+] {name} results saved to {output_file}")

# 1. assetfinder
run_tool("assetfinder", f"{tools['assetfinder']} --subs-only {domain}", f"{output_dir}/assetfinder.txt")

# 2. subfinder
run_tool("subfinder", f"{tools['subfinder']} -d {domain} -silent", f"{output_dir}/subfinder.txt")

# 3. amass
run_tool("amass", f"{tools['amass']} enum -d {domain} -norecursive -nolocaldb", f"{output_dir}/amass.txt")

# Combine and deduplicate subdomains
print("[+] Merging and deduplicating subdomains...")
all_subs_path = f"{output_dir}/all_subdomains.txt"
subprocess.run(f"cat {output_dir}/*.txt | sort -u > {all_subs_path}", shell=True)
print(f"[+] All unique subdomains saved to {all_subs_path}")

# 4. gau for URL/parameter discovery
print("[+] Running gau to get URLs with parameters...")
gau_output = f"{output_dir}/gau_output.txt"
subprocess.run(f"{tools['gau']} {domain} > {gau_output}", shell=True)

# Extract unique parameters
print("[+] Extracting unique parameters from gau output...")
params_output = f"{output_dir}/unique_params.txt"
subprocess.run(f"cat {gau_output} | grep '?'' | cut -d '?' -f2 | tr '&' '\\n' | cut -d '=' -f1 | sort -u > {params_output}", shell=True)
print(f"[+] Unique parameters saved to {params_output}")

print("\n[✔] Subdomain enumeration and parameter extraction complete!")
