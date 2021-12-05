import csv
import json
import sys
import argparse
import re
import requests
import time


def query(gene_name):
    url = "http://www.proteinatlas.org/api/search_download.php"
    response = requests.get(url, params={
        "search": gene_name,
        "format": "json",
        "columns": "g,gs,di,pe,scml,scal,relc",
        "compress": "no"        
    })
    response.raise_for_status()
    return json.loads(response.text)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("names")
    args = parser.parse_args()
    results = []
    with open(args.names) as f:
        for row in csv.reader(f):
            row_id, gene = row
            try:
                print("Querying: {}".format(gene))
                result = query(gene)
                output = {
                    "row": row_id,
                    "gene_name": gene,
                    "result": result
                }
                results.append(output)
            except Exception as e:
                sys.stderr.write(
                    "Failed to find result for: {} (GN={}), Error={}\n".format(row_id, gene, e)
                )
                
            # Don't hammer the API
            time.sleep(0.5)
            
    with open("query_results.json", "w") as f:
        f.write(json.dumps(results))


if __name__ == "__main__":
    main()
