import time

import httpx

from schemas import PoliticianRecord


def fetch_one_politician(politician_id: str) -> PoliticianRecord | None:
    url = "https://query.wikidata.org/sparql"
    query = f"""
        SELECT ?politician ?politicianLabel ?positionLabel ?partyLabel ?countryLabel ?facebook ?instagram ?twitter
        WHERE {{
          BIND(wd:{politician_id} AS ?politician) .
          wd:{politician_id} rdfs:label ?politicianLabel .
          FILTER(LANG(?politicianLabel) = "en")

          OPTIONAL {{
            ?politician p:P39 ?statement .
            ?statement ps:P39 ?position ;
                       pq:P580 ?start_date .

            ?position wdt:P279* wd:Q82955 ;  # Politician occupation
                      rdfs:label ?positionLabel .
            FILTER(LANG(?positionLabel) = "en")

            OPTIONAL {{
              ?statement pq:P4100 ?party .
              ?party rdfs:label ?partyLabel .
              FILTER(LANG(?partyLabel) = "en")
            }}

            OPTIONAL {{
              ?politician wdt:P27 ?country .
              ?country rdfs:label ?countryLabel .
              FILTER(LANG(?countryLabel) = "en")
            }}

            OPTIONAL {{
              ?politician wdt:P2013 ?facebook .
            }}

            OPTIONAL {{
              ?politician wdt:P2003 ?instagram .
            }}

            OPTIONAL {{
              ?politician wdt:P2002 ?twitter .
            }}
          }}

          SERVICE wikibase:label {{ bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }}
        }}
        ORDER BY DESC(?start_date)
        LIMIT 1
        """
    r = httpx.get(url, params={"format": "json", "query": query}, timeout=120)
    if r.status_code != 200:
        print("negative code", r.status_code)
        print("test", r.content)
        time.sleep(2)
        return None
    data = r.json()
    if not data["results"]["bindings"]:
        return None
    item = data["results"]["bindings"][0]
    return PoliticianRecord(
        id=politician_id,
        label="politician",
        literal=item["politicianLabel"]["value"],
        uri=item["politician"]["value"],
        politicianLabel=item.get("politicianLabel", {}).get("value", ""),
        positionLabel=item.get("positionLabel", {}).get("value", ""),
        countryLabel=item.get("countryLabel", {}).get("value", ""),
        partyLabel=item.get("partyLabel", {}).get("value", ""),
        twitter=item.get("twitter", {}).get("value", ""),
        instagram=item.get("instagram", {}).get("value", ""),
        facebook=item.get("facebook", {}).get("value", ""),
    )
