import csv
import json
import sys
import argparse
import re
import requests
import time

def parse_desc(desc):
    matches = re.split("([A-Z]+=)", desc)
    prefix = matches[0].strip()
    raw_attrs = iter(matches[1:])
    attrs = {
        name.strip("=").strip(): value.strip()
        for name, value in zip(raw_attrs, raw_attrs)
    }
    return prefix, attrs
    
def parse_input_no_gn_col(f):
    reader = csv.reader(f)    
    for line in reader:
        row_id = line[0].strip()
        desc = line[1]
        prefix, attrs = parse_desc(desc)
        yield (row_id, attrs.get("GN"))

def parse_input_gn_col(f):
    reader = csv.reader(f)
    
    for line in reader:
        row_id = line[0].strip()
        gene_name = line[1].strip()
        if gene_name:
            yield (row_id, gene_name)
        else:
            desc = line[2]
            prefix, attrs = parse_desc(desc)
            yield (row_id, attrs.get("GN"))

        
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("nogn")
    parser.add_argument("gn")    
    args = parser.parse_args()
    results = []

    with open(args.nogn) as f:
        results += list(parse_input_no_gn_col(f))
    with open(args.gn) as f:
        results += list(parse_input_gn_col(f))

    with open("gene_names.csv", "w") as f:
        out = csv.writer(f)    
        for result in results:
            out.writerow(list(result))

if __name__ == "__main__":
    main()
