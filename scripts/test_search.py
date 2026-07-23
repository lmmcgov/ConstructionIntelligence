from construction_intelligence.ingestion.web.searxng_search_provider import (
    SearXNGSearchProvider,
)


provider = SearXNGSearchProvider(
    pages=5
)


query = (
    '"Horizon Drive" construction '
    'Grand Junction Colorado'
)


urls = provider.search(
    query
)


print()
print("RESULT COUNT")
print("----------------")
print(len(urls))


for url in urls:
    print(url)