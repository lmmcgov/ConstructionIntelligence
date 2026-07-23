from pprint import pprint

from construction_intelligence.ingestion.osm.extractor import (
    OSMConstructionExtractor,
)


def main() -> None:
    extractor = OSMConstructionExtractor()

    ways = extractor.extract("data/raw/GJ.osm.pbf")

    print(f"Found {len(ways)} construction ways.")

    for i, way in enumerate(ways, start=1):
        print(f"\nWay {i}")
        print(f"OSM ID: {way.osm_id}")
        pprint(way.tags)


if __name__ == "__main__":
    main()