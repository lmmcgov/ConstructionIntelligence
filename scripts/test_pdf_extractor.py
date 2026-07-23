from construction_intelligence.ingestion.web.pdf_extractor import (
    PDFExtractor,
)


def main():

    extractor = PDFExtractor()

    url = (
        "https://www.gjcity.org/"
        "DocumentCenter/View/14858/"
        "Grand-Junction-Begins-Construction-at-Horizon-Drive-and-G-Road--PDF"
    )

    document = extractor.extract(
        url
    )

    print()
    print("TITLE")
    print("-----")
    print(document.title)

    print()
    print("CONTENT PREVIEW")
    print("----------------")
    print(
        document.content[:1000]
    )


if __name__ == "__main__":
    main()