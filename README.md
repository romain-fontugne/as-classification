# as-classification

## Tier-1

Obtained from bgp.tools: https://bgp.tools/kb/what-is-a-upstream

## International transits

Obtained with the following IYP query:
```cypher
MATCH (a:AS)<-[d:DEPENDS_ON]-(c:AS)-[cr:COUNTRY {reference_org:'NRO'}]-(cc:Country),
(a)-[:PEERS_WITH]-(c)
WHERE a<>c AND d.hege > 0.5 AND cc.country_code <> 'ZZ'
WITH a, COUNT(DISTINCT cc.country_code) AS nb_countries
WHERE nb_countries > 1
RETURN a.asn AS asn
```

## Domestic transits
Obtained with the following IYP query:
```cypher
MATCH (a:AS)<-[d:DEPENDS_ON]-(c:AS)-[cr:COUNTRY {reference_org:'NRO'}]-(cc:Country),
(a)-[:PEERS_WITH]-(c)
WHERE a<>c AND d.hege > 0.5 AND cc.country_code <> 'ZZ'
WITH a, COUNT(DISTINCT cc.country_code) AS nb_countries
WHERE nb_countries = 1
RETURN a.asn AS asn
```

## Hypergiants
Obtained with the following IYP query:
```cypher
MATCH (a:AS)-[:MEMBER_OF]-(ix:IXP)
WITH a, COUNT(DISTINCT ix) as nb_ixps
WHERE  nb_ixps > 50
RETURN a.asn AS asn
```

## List of all active ASNs

```cypher
MATCH (a:AS) RETURN a.asn AS asn
``
