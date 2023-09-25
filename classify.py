from neo4j import GraphDatabase


URI = "neo4j://iyp.iijlab.net:7687"
AUTH = ("neo4j", "password")

TIER1 = [6762, 12956, 2914, 3356, 6453, 701, 6461, 3257, 1299, 3491, 7018, 3320, 5511, 6830, 7922, 174, 6939]

HYPERGIANT = """
    MATCH (a:AS)-[:MEMBER_OF]-(ix:IXP)
    WITH a, COUNT(DISTINCT ix) as nb_ixps
    WHERE  nb_ixps > 50
    RETURN a.asn AS asn
"""

INTERNATIONAL = """
    MATCH (a:AS)<-[d:DEPENDS_ON]-(c:AS)-[cr:COUNTRY {reference_org:'NRO'}]-(cc:Country),
    (a)-[:PEERS_WITH]-(c)
    WHERE a<>c AND d.hege > 0.5 AND cc.country_code <> 'ZZ'
    WITH a, COUNT(DISTINCT cc.country_code) AS nb_countries
    WHERE nb_countries > 1
    RETURN a.asn AS asn
"""

DOMESTIC = """
    MATCH (a:AS)<-[d:DEPENDS_ON]-(c:AS)-[cr:COUNTRY {reference_org:'NRO'}]-(cc:Country),
    (a)-[:PEERS_WITH]-(c)
    WHERE a<>c AND d.hege > 0.5 AND cc.country_code <> 'ZZ'
    WITH a, COUNT(DISTINCT cc.country_code) AS nb_countries
    WHERE nb_countries = 1
    RETURN a.asn AS asn
"""

ALL = "MATCH (a:AS) RETURN a.asn AS asn"


with GraphDatabase.driver(URI, auth=AUTH) as driver:

    results = {}

    # Get all ASes
    rec, _, _ = driver.execute_query(ALL, database_="neo4j")
    for record in rec:
        results[record['asn']] = 'stub'

    # Add domestic transits
    rec, _, _ = driver.execute_query(DOMESTIC, database_="neo4j")
    for record in rec:
        results[record['asn']] = 'domestic'

    # Add international transits
    rec, _, _ = driver.execute_query(INTERNATIONAL, database_="neo4j")
    for record in rec:
        results[record['asn']] = 'international'

    # Add hypergiants
    rec, _, _ = driver.execute_query(HYPERGIANT, database_="neo4j")
    for record in rec:
        results[record['asn']] = 'hypergiant'

    # Add Tier-1
    for asn in TIER1:
        results[asn] = 'tier1'

    # Print results
    for asn, classif in results.items():
        print(f'{asn}, {classif}')
