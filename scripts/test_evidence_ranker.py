from construction_intelligence.ingestion.web.evidence_ranker import (
    EvidenceRanker,
)

from construction_intelligence.core.project import Project


project = Project(
    name="Horizon Drive G Road Roundabout",
    city="Grand Junction",
    state="Colorado",
    country="United States",
    road_name="Horizon Drive",
)


urls = [
    "https://www.kjct8.com/2025/10/01/horizon-drive-g-road-roundabout-nearing-completion/",
    "https://www.horizonblue.com/",
    "https://www.gjcity.org/CivicAlerts.asp?AID=1722&ARC=2428",
    "https://www.gjcity.org/DocumentCenter/View/14858/Grand-Junction-Begins-Construction-at-Horizon-Drive-and-G-Road--PDF",
    "https://www.playstation.com/en-us/horizon/",
]


ranker = EvidenceRanker()

results = ranker.rank_with_details(
    urls,
    project,
)


for result in results:
    print()
    print(result.score)
    print(result.url)

    for reason in result.reasons:
        print(" -", reason)