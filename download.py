import argparse
import csv
from neo4j import GraphDatabase
import yaml


def run_query_and_export_to_csv(uri: str, user: str, password: str, query: str, csv_path: str) -> None:
    driver = GraphDatabase.driver(uri, auth=(user, password))

    with driver.session() as session:
        # Query IYP
        result = session.run(query)

        # Fetch records
        records = result.data()

        if not records:
            print("No data returned by query.")
            return

        # Extract column names from keys of the first record
        column_names = records[0].keys()

        # Write to CSV
        with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=column_names)
            writer.writeheader()
            for row in records:
                writer.writerow(row)

        print(f"Query results saved to {csv_path}")

    driver.close()


if __name__ == '__main__':

    # CLI interface
    parser = argparse.ArgumentParser(
            description="Execute given IYP query and save results in a file.")
    parser.add_argument('configuration_file', help='YAML file providing all parameters.')
    args = parser.parse_args()

    # Open and read the configuration YAML file
    with open(args.configuration_file, 'r') as file:
        config = yaml.safe_load(file)

    # Fetch all parameters
    uri = config['iyp']['server']
    username = config['iyp']['username']
    password = config['iyp']['password']
    query = config['query']
    output = config['output_fname']

    # Execute the query and save results
    run_query_and_export_to_csv(uri, username, password, query, output)
