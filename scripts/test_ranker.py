from construction_intelligence.ingestion.web.evidence_ranker import (
    EvidenceRanker,
)

from construction_intelligence.core.project import (
    Project,
)


project = Project(
    name="Horizon Glen Drive Improvements",
    aliases=[
        "Horizon Drive",
        "Horizon Drive and G Road",
    ],
    city="Grand Junction",
    state="Colorado",
    country="United States",
    road_name="Horizon Glen Drive",
)


urls = [
    "https://www.gjcity.org/515/Horizon-Drive-Business-Improvement",
    "https://shawconstruction.net/projects/760-horizon-drive",
    "https://www.horizonblue.com",
    "https://playstation.com/en-us/horizon/",
]


ranker = EvidenceRanker(
    max_results=50
)


for item in ranker.rank_with_details(
    urls,
    project,
):

    print()
    print(item.score)
    print(item.url)

    for reason in item.reasons:
        print("-", reason)