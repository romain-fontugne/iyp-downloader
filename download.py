from neo4j import GraphDatabase
import csv

# Neo4j connection details
NEO4J_URI = "bolt://localhost:7687"  
USERNAME = "neo4j"
PASSWORD = "password"

# All prefixes announced on BGP with corresponding ASN and Opaque IDs
CYPHER_QUERY = """
MATCH (a:AS)-[:ORIGINATE {reference_org: 'BGPKIT'}]-(p:BGPPrefix)
OPTIONAL MATCH (a)-[:ASSIGNED]-(oid_as:OpaqueID)
OPTIONAL MATCH (p)-[:ASSIGNED]-(oid_pfx:OpaqueID)
RETURN DISTINCT a.asn, oid_as.id, p.prefix, oid_pfx.prefix
"""

# CAIDA AS relationship for IPv4
CYPHER_QUERY = """
MATCH (as_a:AS)-[link:PEERS_WITH {reference_name:'caida.as_relationships_v4'}]->(as_b:AS)
RETURN DISTINCT as_a.asn, as_b.asn, link.rel;
"""

# CAIDA AS relationship for IPv4 in Japan
CYPHER_QUERY_JP = """
MATCH (:Country {country_code:'JP'})-[:COUNTRY {reference_name:'nro.delegated_stats'}]-(as_a:AS)-[link:PEERS_WITH {reference_name:'caida.as_relationships_v4'}]->(as_b:AS)-[:COUNTRY {reference_name:'nro.delegated_stats'}]-(:Country {country_code:'JP'})
RETURN DISTINCT as_a.asn, as_b.asn, link.rel
"""

# AS names, registered country, and RIR
CYPHER_QUERY = """
MATCH (a:AS)
OPTIONAL MATCH (a)-[:NAME {reference_org:'PeeringDB'}]->(pdbn:Name)
OPTIONAL MATCH (a)-[:NAME {reference_org:'BGP.Tools'}]->(btn:Name)
OPTIONAL MATCH (a)-[:NAME {reference_org:'RIPE NCC'}]->(ripen:Name)
OPTIONAL MATCH (a)-[cr:COUNTRY {reference_name: 'nro.delegated_stats'}]-(cc:Country)
RETURN DISTINCT a.asn AS asn, COALESCE(pdbn.name, btn.name, ripen.name) AS name, cc.country_code AS country_code, cr.registry as rir
"""

# Output CSV file
CSV_FILE_PATH = "iyp_query_results.csv"


def run_query_and_export_to_csv(uri, user, password, query, csv_path):
    driver = GraphDatabase.driver(uri, auth=(user, password))

    with driver.session() as session:
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

# Run the function
run_query_and_export_to_csv(NEO4J_URI, USERNAME, PASSWORD, CYPHER_QUERY, CSV_FILE_PATH)

