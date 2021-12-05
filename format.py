import csv
import json
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query_results")
    args = parser.parse_args()
    results = []
    with open(args.query_results) as f:
        data = json.load(f)
        result_cols = set()
        result_rows = []
        for item in data:
            results = item["result"]
            row = {}
            row["row"] = item["row"]
            row["gene_name"] = item["gene_name"]
            if len(results) > 0:
                result = item["result"][0]
                keys = result.keys()
                result_cols = result_cols.union(set(keys))
                for key in keys:
                    row[key] = str(result[key]) 
            result_rows.append(row)

    with open("query_results.csv", "w") as f:
        writer = csv.DictWriter(f, fieldnames=["row", "gene_name"] + sorted(list(result_cols)))
        writer.writeheader()
        for row in result_rows:
            writer.writerow(row)
        
                
if __name__ == "__main__":
    main()
