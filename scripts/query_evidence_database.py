from construction_intelligence.database.sqlite import Database


def main() -> None:

    database = Database(
        "construction_intelligence.db"
    )

    cursor = database.query(
        """
        SELECT
            p.name,
            ee.overall_score,
            er.source_name,
            er.title,
            er.url
        FROM evidence_evaluations ee
        JOIN evidence_resources er
            ON er.evaluation_id = ee.id
        JOIN projects p
            ON p.id = ee.project_id;
        """
    )

    print(
        "Evidence database contents"
    )
    print(
        "-------------------------"
    )

    for row in cursor.fetchall():

        print(
            f"Project: {row['name']}"
        )

        print(
            f"Confidence: {row['overall_score']}"
        )

        print(
            "Resource:"
        )

        print(
            f"- {row['source_name']}"
        )

        print(
            f"- {row['title']}"
        )

        print(
            f"- {row['url']}"
        )

        print()


if __name__ == "__main__":
    main()