"""
International country search profiles.

Localized construction intelligence profiles
used by:

- SearchContextProvider
- EvidenceDiscoveryService
- EvidenceRanker
- query generation
- extraction fallback selection

Profiles contain:

- language
- region
- construction terminology
- infrastructure terminology
- procurement terminology
- government terminology
- official organizations
- government domains
- news indicators
- negative filtering terms
- search intent vocabulary
- source priority weighting
"""

from __future__ import annotations


from construction_intelligence.ingestion.web.search_context import (
    SearchContext,
)


# ==========================================================
# Profile factory
# ==========================================================


def create_profile(
    *,
    country: str,
    language: str,
    region: str,
    construction_terms: list[str],
    infrastructure_terms: list[str],
    procurement_terms: list[str],
    government_terms: list[str],
    official_source_terms: list[str],
    government_domains: list[str],
    news_terms: list[str],
    negative_terms: list[str],
    search_intents: list[str],
    source_priority: dict[str, int],
) -> SearchContext:
    """
    Create a localized SearchContext profile.
    """

    return SearchContext(
        country=country,
        language=language,
        region=region,

        construction_terms=construction_terms,
        infrastructure_terms=infrastructure_terms,
        procurement_terms=procurement_terms,

        government_terms=government_terms,
        official_source_terms=official_source_terms,
        government_domains=government_domains,

        news_terms=news_terms,
        negative_terms=negative_terms,

        search_intents=search_intents,
        source_priority=source_priority,
    )


# ==========================================================
# Global search intent vocabulary
# ==========================================================


DEFAULT_SEARCH_INTENTS = [
    "construction",
    "project",
    "infrastructure",
    "development",

    "design",
    "planning",
    "phase",

    "contract",
    "bid",
    "tender",
    "procurement",
    "award",

    "announcement",
    "breaking ground",
    "construction begins",
    "completion",
    "opening",
]


# ==========================================================
# Evidence source weighting
# ==========================================================


DEFAULT_SOURCE_PRIORITY = {

    #
    # Highest confidence
    #
    "government": 20,

    "procurement": 18,


    #
    # Useful secondary evidence
    #
    "news": 10,

    "academic": 8,

    "developer": 5,


    #
    # Weak or problematic sources
    #
    "social_media": -10,

    "real_estate": -15,

    "commercial_listing": -15,

}


# ==========================================================
# Country aliases
# ==========================================================


COUNTRY_ALIASES = {

    #
    # United States
    #

    "usa": "united states",

    "us": "united states",

    "u.s.": "united states",

    "america": "united states",

    "united states of america": "united states",


    #
    # Brazil
    #

    "brasil": "brazil",


    #
    # Mexico
    #

    "méxico": "mexico",


    #
    # South Korea
    #

    "korea": "south korea",

    "republic of korea": "south korea",


    #
    # Czech Republic
    #

    "czechia": "czech republic",


    #
    # Romania
    #

    "românia": "romania",


    #
    # Türkiye
    #

    "turkiye": "turkey",

    "türkiye": "turkey",


    #
    # Dominican Republic
    #

    "republica dominicana": "dominican republic",


    #
    # United Kingdom
    #

    "uk": "united kingdom",

    "britain": "united kingdom",

}


# ==========================================================
# Shared language vocabularies
# ==========================================================


# ----------------------------------------------------------
# English
# ----------------------------------------------------------


ENGLISH_CONSTRUCTION = [

    "construction",

    "infrastructure",

    "project",

    "development",

    "public works",

    "capital improvement",

    "civil works",

]


ENGLISH_INFRASTRUCTURE = [

    "road",

    "highway",

    "bridge",

    "transportation",

    "corridor",

    "road improvement",

    "road widening",

    "intersection",

]


ENGLISH_PROCUREMENT = [

    "bid",

    "tender",

    "contract",

    "procurement",

    "award",

    "RFP",

    "RFQ",

]


ENGLISH_GOVERNMENT = [

    "government",

    "municipality",

    "department",

    "agency",

    "authority",

    "council",

]


ENGLISH_NEGATIVE = [

    "movie",

    "film",

    "bank",

    "property",

    "real estate",

    "game",

    "celebrity",

]


ENGLISH_NEWS = [

    "news",

    "journal",

    "times",

    "gazette",

    "daily",

]



# ----------------------------------------------------------
# Spanish
# ----------------------------------------------------------


SPANISH_CONSTRUCTION = [

    "construcción",

    "obra",

    "infraestructura",

    "proyecto",

    "desarrollo",

    "trabajos",

]


SPANISH_INFRASTRUCTURE = [

    "carretera",

    "camino",

    "vía",

    "calle",

    "pavimentación",

    "rehabilitación",

    "puente",

    "corredor vial",

]


SPANISH_PROCUREMENT = [

    "licitación",

    "contrato",

    "adjudicación",

    "concurso",

    "contratación pública",

]


SPANISH_GOVERNMENT = [

    "gobierno",

    "municipalidad",

    "alcaldía",

    "ministerio",

    "secretaría",

]


SPANISH_NEGATIVE = [

    "película",

    "banco",

    "inmueble",

    "apartamento",

    "juego",

]


SPANISH_NEWS = [

    "noticias",

    "diario",

    "prensa",

]



# ----------------------------------------------------------
# Portuguese
# ----------------------------------------------------------


PORTUGUESE_CONSTRUCTION = [

    "obra",

    "construção",

    "infraestrutura",

    "projeto",

    "desenvolvimento",

    "obras públicas",

]


PORTUGUESE_INFRASTRUCTURE = [

    "rodovia",

    "estrada",

    "rua",

    "ponte",

    "pavimentação",

    "mobilidade",

]


PORTUGUESE_PROCUREMENT = [

    "licitação",

    "edital",

    "contrato",

    "pregão",

    "concorrência",

]


PORTUGUESE_GOVERNMENT = [

    "governo",

    "prefeitura",

    "município",

    "secretaria",

]


PORTUGUESE_NEGATIVE = [

    "imóvel",

    "apartamento",

    "filme",

    "jogo",

]


PORTUGUESE_NEWS = [

    "notícia",

    "jornal",

    "diário",

]



# ----------------------------------------------------------
# French
# ----------------------------------------------------------


FRENCH_CONSTRUCTION = [

    "construction",

    "travaux",

    "infrastructure",

    "projet",

    "aménagement",

]


FRENCH_INFRASTRUCTURE = [

    "route",

    "pont",

    "autoroute",

    "voirie",

    "transport",

]


FRENCH_PROCUREMENT = [

    "appel d'offres",

    "marché public",

    "contrat",

    "soumission",

]


FRENCH_GOVERNMENT = [

    "gouvernement",

    "mairie",

    "ministère",

    "collectivité",

]


FRENCH_NEGATIVE = [

    "film",

    "banque",

    "immobilier",

    "jeu",

]


FRENCH_NEWS = [

    "actualité",

    "journal",

    "presse",

]


# ==========================================================
# End Section 1
# ==========================================================

# ==========================================================
# Additional shared language vocabularies
# ==========================================================


# ----------------------------------------------------------
# German
# ----------------------------------------------------------


GERMAN_CONSTRUCTION = [

    "bau",

    "bauprojekt",

    "infrastruktur",

    "baumaßnahme",

    "bauarbeiten",

]


GERMAN_INFRASTRUCTURE = [

    "straße",

    "autobahn",

    "brücke",

    "verkehr",

    "verkehrsinfrastruktur",

]


GERMAN_PROCUREMENT = [

    "ausschreibung",

    "auftrag",

    "vergabeverfahren",

    "vertrag",

]


GERMAN_GOVERNMENT = [

    "regierung",

    "stadt",

    "gemeinde",

    "behörde",

]


GERMAN_NEGATIVE = [

    "film",

    "bank",

    "immobilien",

    "spiel",

]


GERMAN_NEWS = [

    "nachrichten",

    "zeitung",

    "presse",

]



# ----------------------------------------------------------
# Romanian
# ----------------------------------------------------------


ROMANIAN_CONSTRUCTION = [

    "construcție",

    "lucrări",

    "infrastructură",

    "proiect",

    "dezvoltare",

]


ROMANIAN_INFRASTRUCTURE = [

    "drum",

    "șosea",

    "pod",

    "reabilitare",

    "modernizare",

]


ROMANIAN_PROCUREMENT = [

    "licitație",

    "achiziție",

    "contract",

    "atribuire",

]


ROMANIAN_GOVERNMENT = [

    "guvern",

    "primărie",

    "consiliu local",

    "minister",

]


ROMANIAN_NEGATIVE = [

    "film",

    "bancă",

    "imobil",

    "joc",

]


ROMANIAN_NEWS = [

    "știri",

    "ziar",

    "presa",

]



# ----------------------------------------------------------
# Turkish
# ----------------------------------------------------------


TURKISH_CONSTRUCTION = [

    "inşaat",

    "altyapı",

    "proje",

    "yapım",

    "çalışma",

]


TURKISH_INFRASTRUCTURE = [

    "yol",

    "köprü",

    "karayolu",

    "ulaşım",

]


TURKISH_PROCUREMENT = [

    "ihale",

    "sözleşme",

    "kamu ihalesi",

]


TURKISH_GOVERNMENT = [

    "belediye",

    "bakanlık",

    "devlet",

]


TURKISH_NEGATIVE = [

    "film",

    "banka",

    "emlak",

    "oyun",

]



# ----------------------------------------------------------
# Indonesian
# ----------------------------------------------------------


INDONESIAN_CONSTRUCTION = [

    "pembangunan",

    "konstruksi",

    "proyek",

    "infrastruktur",

]


INDONESIAN_INFRASTRUCTURE = [

    "jalan",

    "jembatan",

    "transportasi",

    "pelebaran jalan",

    "perbaikan jalan",

]


INDONESIAN_PROCUREMENT = [

    "lelang",

    "pengadaan",

    "kontrak",

    "tender",

]


INDONESIAN_GOVERNMENT = [

    "pemerintah",

    "kota",

    "kabupaten",

    "dinas",

]


INDONESIAN_NEGATIVE = [

    "film",

    "game",

    "bank",

    "rumah",

]



# ----------------------------------------------------------
# Vietnamese
# ----------------------------------------------------------


VIETNAMESE_CONSTRUCTION = [

    "xây dựng",

    "công trình",

    "hạ tầng",

    "dự án",

]


VIETNAMESE_INFRASTRUCTURE = [

    "đường",

    "cầu",

    "giao thông",

    "cao tốc",

]


VIETNAMESE_PROCUREMENT = [

    "đấu thầu",

    "gói thầu",

    "hợp đồng",

]


VIETNAMESE_GOVERNMENT = [

    "chính phủ",

    "ủy ban",

    "sở",

]


VIETNAMESE_NEGATIVE = [

    "phim",

    "ngân hàng",

    "bất động sản",

    "game",

]



# ----------------------------------------------------------
# Thai
# ----------------------------------------------------------


THAI_CONSTRUCTION = [

    "ก่อสร้าง",

    "โครงการ",

    "โครงสร้างพื้นฐาน",

]


THAI_INFRASTRUCTURE = [

    "ถนน",

    "สะพาน",

    "คมนาคม",

]


THAI_PROCUREMENT = [

    "จัดซื้อจัดจ้าง",

    "ประมูล",

    "สัญญา",

]


THAI_GOVERNMENT = [

    "รัฐบาล",

    "เทศบาล",

    "กระทรวง",

]


THAI_NEGATIVE = [

    "ภาพยนตร์",

    "ธนาคาร",

    "อสังหาริมทรัพย์",

    "เกม",

]



# ----------------------------------------------------------
# Hindi / Urdu / South Asia
# ----------------------------------------------------------


HINDI_CONSTRUCTION = [

    "निर्माण",

    "परियोजना",

    "बुनियादी ढांचा",

    "विकास",

]


HINDI_INFRASTRUCTURE = [

    "सड़क",

    "पुल",

    "राजमार्ग",

    "परिवहन",

]


HINDI_PROCUREMENT = [

    "निविदा",

    "ठेका",

    "अनुबंध",

]


URDU_CONSTRUCTION = [

    "تعمیر",

    "منصوبہ",

    "ترقیاتی منصوبہ",

    "انفراسٹرکچر",

]


URDU_INFRASTRUCTURE = [

    "سڑک",

    "پل",

    "شاہراہ",

]


URDU_PROCUREMENT = [

    "بولی",

    "ٹینڈر",

    "معاہدہ",

]



# ==========================================================
# Regional fallback profiles
# ==========================================================


REGIONAL_PROFILES = {


    "latin america": create_profile(

        country="Latin America",

        language="es",

        region="latin america",

        construction_terms=SPANISH_CONSTRUCTION,

        infrastructure_terms=SPANISH_INFRASTRUCTURE,

        procurement_terms=SPANISH_PROCUREMENT,

        government_terms=SPANISH_GOVERNMENT,

        official_source_terms=[

            "municipalidad",

            "ministerio",

            "obras públicas",

        ],

        government_domains=[

            ".gob",

            ".gov",

        ],

        news_terms=SPANISH_NEWS,

        negative_terms=SPANISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "anglophone africa": create_profile(

        country="Anglophone Africa",

        language="en",

        region="africa",

        construction_terms=ENGLISH_CONSTRUCTION,

        infrastructure_terms=ENGLISH_INFRASTRUCTURE,

        procurement_terms=ENGLISH_PROCUREMENT,

        government_terms=ENGLISH_GOVERNMENT,

        official_source_terms=[

            "municipality",

            "county government",

            "district assembly",

            "ministry of works",

        ],

        government_domains=[

            ".gov",

            ".go",

        ],

        news_terms=ENGLISH_NEWS,

        negative_terms=ENGLISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "francophone africa": create_profile(

        country="Francophone Africa",

        language="fr",

        region="africa",

        construction_terms=FRENCH_CONSTRUCTION,

        infrastructure_terms=FRENCH_INFRASTRUCTURE,

        procurement_terms=FRENCH_PROCUREMENT,

        government_terms=FRENCH_GOVERNMENT,

        official_source_terms=[

            "mairie",

            "ministère",

            "travaux publics",

        ],

        government_domains=[

            ".gouv",

        ],

        news_terms=FRENCH_NEWS,

        negative_terms=FRENCH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "southeast asia": create_profile(

        country="Southeast Asia",

        language="en",

        region="asia",

        construction_terms=ENGLISH_CONSTRUCTION,

        infrastructure_terms=ENGLISH_INFRASTRUCTURE,

        procurement_terms=ENGLISH_PROCUREMENT,

        government_terms=ENGLISH_GOVERNMENT,

        official_source_terms=[

            "public works",

            "transport department",

            "local government",

        ],

        government_domains=[

            ".gov",

            ".go",

        ],

        news_terms=ENGLISH_NEWS,

        negative_terms=ENGLISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),

}


# ==========================================================
# End Section 2
# ==========================================================

# ==========================================================
# Country Profiles
# ==========================================================


COUNTRY_PROFILES = {


    # ======================================================
    # North America
    # ======================================================


    "united states": create_profile(

        country="United States",

        language="en",

        region="north america",

        construction_terms=ENGLISH_CONSTRUCTION,

        infrastructure_terms=ENGLISH_INFRASTRUCTURE,

        procurement_terms=ENGLISH_PROCUREMENT,

        government_terms=ENGLISH_GOVERNMENT,

        official_source_terms=[

            "city council",

            "public works",

            "department of transportation",

            "county government",

            "municipality",

        ],

        government_domains=[

            ".gov",

        ],

        news_terms=ENGLISH_NEWS,

        negative_terms=ENGLISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "mexico": create_profile(

        country="Mexico",

        language="es",

        region="latin america",

        construction_terms=SPANISH_CONSTRUCTION,

        infrastructure_terms=SPANISH_INFRASTRUCTURE,

        procurement_terms=SPANISH_PROCUREMENT,

        government_terms=SPANISH_GOVERNMENT,

        official_source_terms=[

            "ayuntamiento",

            "municipio",

            "secretaría de infraestructura",

            "SICT",

            "obras públicas",

        ],

        government_domains=[

            ".gob.mx",

        ],

        news_terms=SPANISH_NEWS,

        negative_terms=SPANISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    # ======================================================
    # Central America
    # ======================================================


    "guatemala": create_profile(

        country="Guatemala",

        language="es",

        region="central america",

        construction_terms=SPANISH_CONSTRUCTION,

        infrastructure_terms=SPANISH_INFRASTRUCTURE,

        procurement_terms=SPANISH_PROCUREMENT,

        government_terms=[

            "municipalidad",

            "gobierno",

            "ministerio",

        ],

        official_source_terms=[

            "municipalidad",

            "INFOM",

            "ministerio de comunicaciones",

        ],

        government_domains=[

            ".gob.gt",

        ],

        news_terms=SPANISH_NEWS,

        negative_terms=SPANISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "costa rica": create_profile(

        country="Costa Rica",

        language="es",

        region="central america",

        construction_terms=SPANISH_CONSTRUCTION,

        infrastructure_terms=[

            "carretera",

            "ruta nacional",

            "puente",

            "pavimentación",

            "infraestructura vial",

        ],

        procurement_terms=SPANISH_PROCUREMENT,

        government_terms=[

            "municipalidad",

            "ministerio",

            "gobierno",

        ],

        official_source_terms=[

            "MOPT",

            "municipalidad",

            "CONAVI",

        ],

        government_domains=[

            ".go.cr",

        ],

        news_terms=SPANISH_NEWS,

        negative_terms=SPANISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "panama": create_profile(

        country="Panama",

        language="es",

        region="central america",

        construction_terms=SPANISH_CONSTRUCTION,

        infrastructure_terms=[

            "carretera",

            "corredor",

            "puente",

            "infraestructura vial",

        ],

        procurement_terms=SPANISH_PROCUREMENT,

        government_terms=[

            "municipio",

            "ministerio",

            "gobierno",

        ],

        official_source_terms=[

            "MOP",

            "municipio",

            "contrataciones públicas",

        ],

        government_domains=[

            ".gob.pa",

        ],

        news_terms=SPANISH_NEWS,

        negative_terms=SPANISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    # ======================================================
    # South America
    # ======================================================


    "brazil": create_profile(

        country="Brazil",

        language="pt",

        region="south america",

        construction_terms=PORTUGUESE_CONSTRUCTION,

        infrastructure_terms=PORTUGUESE_INFRASTRUCTURE,

        procurement_terms=[

            "licitação",

            "edital",

            "contrato",

            "pregão",

        ],

        government_terms=[

            "prefeitura",

            "governo",

            "secretaria",

            "município",

        ],

        official_source_terms=[

            "prefeitura",

            "secretaria de obras",

            "DNIT",

            "DER",

            "diário oficial",

        ],

        government_domains=[

            ".gov.br",

        ],

        news_terms=PORTUGUESE_NEWS,

        negative_terms=PORTUGUESE_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "chile": create_profile(

        country="Chile",

        language="es",

        region="south america",

        construction_terms=SPANISH_CONSTRUCTION,

        infrastructure_terms=SPANISH_INFRASTRUCTURE,

        procurement_terms=SPANISH_PROCUREMENT,

        government_terms=SPANISH_GOVERNMENT,

        official_source_terms=[

            "municipalidad",

            "ministerio de obras públicas",

            "MOP",

        ],

        government_domains=[

            ".gob.cl",

        ],

        news_terms=SPANISH_NEWS,

        negative_terms=SPANISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "colombia": create_profile(

        country="Colombia",

        language="es",

        region="south america",

        construction_terms=SPANISH_CONSTRUCTION,

        infrastructure_terms=SPANISH_INFRASTRUCTURE,

        procurement_terms=SPANISH_PROCUREMENT,

        government_terms=SPANISH_GOVERNMENT,

        official_source_terms=[

            "alcaldía",

            "IDU",

            "INVIAS",

            "ANI",

            "secretaría de movilidad",

        ],

        government_domains=[

            ".gov.co",

        ],

        news_terms=SPANISH_NEWS,

        negative_terms=SPANISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "argentina": create_profile(

        country="Argentina",

        language="es",

        region="south america",

        construction_terms=SPANISH_CONSTRUCTION,

        infrastructure_terms=SPANISH_INFRASTRUCTURE,

        procurement_terms=SPANISH_PROCUREMENT,

        government_terms=SPANISH_GOVERNMENT,

        official_source_terms=[

            "municipalidad",

            "vialidad",

            "ministerio de obras públicas",

        ],

        government_domains=[

            ".gob.ar",

        ],

        news_terms=SPANISH_NEWS,

        negative_terms=SPANISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),

# ==========================================================
# Remaining Country Profiles
# ==========================================================


    # ======================================================
    # South America Continued
    # ======================================================


    "peru": create_profile(

        country="Peru",

        language="es",

        region="south america",

        construction_terms=SPANISH_CONSTRUCTION,

        infrastructure_terms=[

            "carretera",

            "camino",

            "puente",

            "vialidad",

            "pavimentación",

        ],

        procurement_terms=SPANISH_PROCUREMENT,

        government_terms=[

            "municipalidad",

            "gobierno regional",

            "ministerio",

        ],

        official_source_terms=[

            "MTC",

            "Provías",

            "municipalidad",

            "OSCE",

        ],

        government_domains=[

            ".gob.pe",

        ],

        news_terms=SPANISH_NEWS,

        negative_terms=SPANISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "ecuador": create_profile(

        country="Ecuador",

        language="es",

        region="south america",

        construction_terms=SPANISH_CONSTRUCTION,

        infrastructure_terms=SPANISH_INFRASTRUCTURE,

        procurement_terms=SPANISH_PROCUREMENT,

        government_terms=SPANISH_GOVERNMENT,

        official_source_terms=[

            "municipio",

            "ministerio de transporte",

            "MTOP",

            "SERCOP",

        ],

        government_domains=[

            ".gob.ec",

        ],

        news_terms=SPANISH_NEWS,

        negative_terms=SPANISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "bolivia": create_profile(

        country="Bolivia",

        language="es",

        region="south america",

        construction_terms=SPANISH_CONSTRUCTION,

        infrastructure_terms=[

            "carretera",

            "camino",

            "puente",

            "infraestructura vial",

        ],

        procurement_terms=SPANISH_PROCUREMENT,

        government_terms=SPANISH_GOVERNMENT,

        official_source_terms=[

            "ABC",

            "municipio",

            "ministerio de obras públicas",

        ],

        government_domains=[

            ".gob.bo",

        ],

        news_terms=SPANISH_NEWS,

        negative_terms=SPANISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "venezuela": create_profile(

        country="Venezuela",

        language="es",

        region="south america",

        construction_terms=SPANISH_CONSTRUCTION,

        infrastructure_terms=SPANISH_INFRASTRUCTURE,

        procurement_terms=SPANISH_PROCUREMENT,

        government_terms=[

            "gobierno",

            "ministerio",

            "alcaldía",

        ],

        official_source_terms=[

            "ministerio de transporte",

            "gobernación",

            "alcaldía",

        ],

        government_domains=[

            ".gob.ve",

        ],

        news_terms=SPANISH_NEWS,

        negative_terms=SPANISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    # ======================================================
    # Caribbean
    # ======================================================


    "dominican republic": create_profile(

        country="Dominican Republic",

        language="es",

        region="caribbean",

        construction_terms=SPANISH_CONSTRUCTION,

        infrastructure_terms=SPANISH_INFRASTRUCTURE,

        procurement_terms=SPANISH_PROCUREMENT,

        government_terms=SPANISH_GOVERNMENT,

        official_source_terms=[

            "ayuntamiento",

            "ministerio de obras públicas",

            "MOPC",

        ],

        government_domains=[

            ".gob.do",

        ],

        news_terms=SPANISH_NEWS,

        negative_terms=SPANISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "haiti": create_profile(

        country="Haiti",

        language="fr",

        region="caribbean",

        construction_terms=FRENCH_CONSTRUCTION,

        infrastructure_terms=FRENCH_INFRASTRUCTURE,

        procurement_terms=FRENCH_PROCUREMENT,

        government_terms=FRENCH_GOVERNMENT,

        official_source_terms=[

            "mairie",

            "ministère des travaux publics",

            "MTPTC",

        ],

        government_domains=[

            ".gouv.ht",

        ],

        news_terms=FRENCH_NEWS,

        negative_terms=FRENCH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "jamaica": create_profile(

        country="Jamaica",

        language="en",

        region="caribbean",

        construction_terms=ENGLISH_CONSTRUCTION,

        infrastructure_terms=ENGLISH_INFRASTRUCTURE,

        procurement_terms=ENGLISH_PROCUREMENT,

        government_terms=ENGLISH_GOVERNMENT,

        official_source_terms=[

            "parish council",

            "National Works Agency",

            "Ministry of Transport",

        ],

        government_domains=[

            ".gov.jm",

        ],

        news_terms=ENGLISH_NEWS,

        negative_terms=ENGLISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    # ======================================================
    # Africa
    # ======================================================


    "ghana": create_profile(

        country="Ghana",

        language="en",

        region="africa",

        construction_terms=ENGLISH_CONSTRUCTION,

        infrastructure_terms=ENGLISH_INFRASTRUCTURE,

        procurement_terms=[

            "tender",

            "contract",

            "procurement",

            "bid",

        ],

        government_terms=[

            "government",

            "assembly",

            "ministry",

        ],

        official_source_terms=[

            "District Assembly",

            "Metropolitan Assembly",

            "Ministry of Roads and Highways",

        ],

        government_domains=[

            ".gov.gh",

        ],

        news_terms=ENGLISH_NEWS,

        negative_terms=ENGLISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "nigeria": create_profile(

        country="Nigeria",

        language="en",

        region="africa",

        construction_terms=ENGLISH_CONSTRUCTION,

        infrastructure_terms=ENGLISH_INFRASTRUCTURE,

        procurement_terms=ENGLISH_PROCUREMENT,

        government_terms=[

            "government",

            "state government",

            "LGA",

            "ministry",

        ],

        official_source_terms=[

            "Federal Ministry of Works",

            "State Ministry of Works",

            "Federal Capital Territory",

            "Local Government Area",

        ],

        government_domains=[

            ".gov.ng",

        ],

        news_terms=ENGLISH_NEWS,

        negative_terms=ENGLISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "kenya": create_profile(

        country="Kenya",

        language="en",

        region="africa",

        construction_terms=ENGLISH_CONSTRUCTION,

        infrastructure_terms=ENGLISH_INFRASTRUCTURE,

        procurement_terms=ENGLISH_PROCUREMENT,

        government_terms=[

            "county government",

            "ministry",

            "authority",

        ],

        official_source_terms=[

            "Kenya Urban Roads Authority",

            "county government",

            "Ministry of Roads",

        ],

        government_domains=[

            ".go.ke",

        ],

        news_terms=ENGLISH_NEWS,

        negative_terms=ENGLISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "tanzania": create_profile(

        country="Tanzania",

        language="en",

        region="africa",

        construction_terms=ENGLISH_CONSTRUCTION,

        infrastructure_terms=ENGLISH_INFRASTRUCTURE,

        procurement_terms=ENGLISH_PROCUREMENT,

        government_terms=[

            "council",

            "ministry",

            "government",

        ],

        official_source_terms=[

            "Tanzania Rural and Urban Roads Agency",

            "municipal council",

            "Ministry of Works",

        ],

        government_domains=[

            ".go.tz",

        ],

        news_terms=ENGLISH_NEWS,

        negative_terms=ENGLISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "uganda": create_profile(

        country="Uganda",

        language="en",

        region="africa",

        construction_terms=ENGLISH_CONSTRUCTION,

        infrastructure_terms=ENGLISH_INFRASTRUCTURE,

        procurement_terms=ENGLISH_PROCUREMENT,

        government_terms=ENGLISH_GOVERNMENT,

        official_source_terms=[

            "district local government",

            "Uganda National Roads Authority",

            "Ministry of Works",

        ],

        government_domains=[

            ".go.ug",

        ],

        news_terms=ENGLISH_NEWS,

        negative_terms=ENGLISH_NEGATIVE,

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),
# ==========================================================
# Asia, Europe, Africa Continued
# ==========================================================


"south africa": create_profile(
    country="South Africa",
    language="en",
    region="africa",

    construction_terms=ENGLISH_CONSTRUCTION,

    infrastructure_terms=[
        "road",
        "highway",
        "bridge",
        "transport infrastructure",
        "public works",
    ],

    procurement_terms=[
        "tender",
        "contract",
        "bid",
        "procurement",
    ],

    government_terms=[
        "municipality",
        "province",
        "department",
        "government",
    ],

    official_source_terms=[
        "municipality",
        "Department of Transport",
        "SANRAL",
        "province",
    ],

    government_domains=[
        ".gov.za",
    ],

    news_terms=ENGLISH_NEWS,

    negative_terms=ENGLISH_NEGATIVE,

    search_intents=DEFAULT_SEARCH_INTENTS,

    source_priority=DEFAULT_SOURCE_PRIORITY,
),



"philippines": create_profile(
    country="Philippines",
    language="en",
    region="asia",

    construction_terms=ENGLISH_CONSTRUCTION,

    infrastructure_terms=[
        "road",
        "bridge",
        "highway",
        "transportation",
        "public works",
    ],

    procurement_terms=[
        "bid",
        "contract",
        "procurement",
        "award",
    ],

    government_terms=[
        "barangay",
        "municipality",
        "city government",
        "department",
    ],

    official_source_terms=[
        "DPWH",
        "LGU",
        "barangay",
        "Department of Transportation",
    ],

    government_domains=[
        ".gov.ph",
    ],

    news_terms=ENGLISH_NEWS,

    negative_terms=ENGLISH_NEGATIVE,

    search_intents=DEFAULT_SEARCH_INTENTS,

    source_priority=DEFAULT_SOURCE_PRIORITY,
),



"pakistan": create_profile(
    country="Pakistan",
    language="ur",
    region="asia",

    construction_terms=[
        "construction",
        "تعمیر",
        "development",
        "ترقیاتی منصوبہ",
    ],

    infrastructure_terms=[
        "road",
        "سڑک",
        "highway",
        "infrastructure",
    ],

    procurement_terms=[
        "tender",
        "contract",
        "بولی",
        "procurement",
    ],

    government_terms=[
        "government",
        "department",
        "ministry",
    ],

    official_source_terms=[
        "National Highway Authority",
        "Pakistan Public Works",
        "provincial government",
    ],

    government_domains=[
        ".gov.pk",
    ],

    news_terms=[
        "news",
        "اخبار",
    ],

    negative_terms=[
        "movie",
        "film",
        "property",
        "bank",
    ],

    search_intents=DEFAULT_SEARCH_INTENTS,

    source_priority=DEFAULT_SOURCE_PRIORITY,
),



"india": create_profile(
    country="India",
    language="hi",
    region="asia",

    construction_terms=[
        "construction",
        "निर्माण",
        "infrastructure",
        "project",
    ],

    infrastructure_terms=[
        "road",
        "highway",
        "सड़क",
        "bridge",
    ],

    procurement_terms=[
        "tender",
        "contract",
        "procurement",
        "निविदा",
    ],

    government_terms=[
        "government",
        "ministry",
        "municipality",
    ],

    official_source_terms=[
        "Municipal Corporation",
        "PWD",
        "National Highways Authority of India",
    ],

    government_domains=[
        ".gov.in",
    ],

    news_terms=[
        "news",
        "समाचार",
    ],

    negative_terms=[
        "movie",
        "film",
        "bank",
        "property",
    ],

    search_intents=DEFAULT_SEARCH_INTENTS,

    source_priority=DEFAULT_SOURCE_PRIORITY,
),



"bangladesh": create_profile(
    country="Bangladesh",
    language="bn",
    region="asia",

    construction_terms=[
        "construction",
        "নির্মাণ",
        "development",
        "project",
    ],

    infrastructure_terms=[
        "road",
        "bridge",
        "highway",
        "সড়ক",
    ],

    procurement_terms=[
        "tender",
        "contract",
        "procurement",
    ],

    government_terms=[
        "government",
        "ministry",
        "city corporation",
    ],

    official_source_terms=[
        "Local Government Engineering Department",
        "Roads and Highways Department",
    ],

    government_domains=[
        ".gov.bd",
    ],

    news_terms=[
        "news",
    ],

    negative_terms=[
        "movie",
        "film",
        "property",
    ],

    search_intents=DEFAULT_SEARCH_INTENTS,

    source_priority=DEFAULT_SOURCE_PRIORITY,
),



"vietnam": create_profile(
    country="Vietnam",
    language="vi",
    region="asia",

    construction_terms=[
        "xây dựng",
        "công trình",
        "hạ tầng",
        "dự án",
    ],

    infrastructure_terms=[
        "đường",
        "cầu",
        "giao thông",
    ],

    procurement_terms=[
        "đấu thầu",
        "hợp đồng",
        "gói thầu",
    ],

    government_terms=[
        "ủy ban nhân dân",
        "bộ",
        "sở",
    ],

    official_source_terms=[
        "Ministry of Transport",
        "People's Committee",
    ],

    government_domains=[
        ".gov.vn",
    ],

    news_terms=[
        "tin tức",
    ],

    negative_terms=[
        "film",
        "movie",
        "bank",
    ],

    search_intents=DEFAULT_SEARCH_INTENTS,

    source_priority=DEFAULT_SOURCE_PRIORITY,
),

# ==========================================================
# Southeast Asia / East Asia
# ==========================================================


"thailand": create_profile(
    country="Thailand",
    language="th",
    region="asia",

    construction_terms=[
        "construction",
        "ก่อสร้าง",
        "โครงการ",
        "โครงสร้างพื้นฐาน",
    ],

    infrastructure_terms=[
        "road",
        "ถนน",
        "highway",
        "bridge",
        "transportation",
    ],

    procurement_terms=[
        "tender",
        "contract",
        "ประกวดราคา",
        "จัดซื้อจัดจ้าง",
    ],

    government_terms=[
        "government",
        "ministry",
        "municipality",
        "จังหวัด",
    ],

    official_source_terms=[
        "Department of Highways",
        "Department of Rural Roads",
        "เทศบาล",
        "กระทรวงคมนาคม",
    ],

    government_domains=[
        ".go.th",
    ],

    news_terms=[
        "ข่าว",
        "news",
    ],

    negative_terms=[
        "movie",
        "film",
        "bank",
        "property",
        "game",
    ],

    search_intents=DEFAULT_SEARCH_INTENTS,

    source_priority=DEFAULT_SOURCE_PRIORITY,
),



"malaysia": create_profile(
    country="Malaysia",
    language="ms",
    region="asia",

    construction_terms=[
        "construction",
        "pembinaan",
        "projek",
        "infrastruktur",
    ],

    infrastructure_terms=[
        "jalan",
        "lebuh raya",
        "jambatan",
        "pengangkutan",
    ],

    procurement_terms=[
        "tender",
        "kontrak",
        "perolehan",
        "sebut harga",
    ],

    government_terms=[
        "kerajaan",
        "jabatan",
        "majlis bandaraya",
    ],

    official_source_terms=[
        "Jabatan Kerja Raya",
        "JKR",
        "Majlis Bandaraya",
        "Kementerian Kerja Raya",
    ],

    government_domains=[
        ".gov.my",
    ],

    news_terms=[
        "berita",
        "news",
    ],

    negative_terms=[
        "movie",
        "film",
        "bank",
        "property",
        "game",
    ],

    search_intents=DEFAULT_SEARCH_INTENTS,

    source_priority=DEFAULT_SOURCE_PRIORITY,
),



"japan": create_profile(
    country="Japan",
    language="ja",
    region="asia",

    construction_terms=[
        "construction",
        "建設",
        "工事",
        "インフラ",
        "事業",
    ],

    infrastructure_terms=[
        "道路",
        "橋",
        "交通",
        "都市整備",
    ],

    procurement_terms=[
        "入札",
        "契約",
        "調達",
    ],

    government_terms=[
        "政府",
        "自治体",
        "市役所",
        "省",
    ],

    official_source_terms=[
        "国土交通省",
        "Ministry of Land Infrastructure Transport and Tourism",
        "市役所",
        "都道府県",
    ],

    government_domains=[
        ".go.jp",
        ".lg.jp",
    ],

    news_terms=[
        "ニュース",
        "新聞",
    ],

    negative_terms=[
        "映画",
        "ゲーム",
        "銀行",
        "不動産",
    ],

    search_intents=DEFAULT_SEARCH_INTENTS,

    source_priority=DEFAULT_SOURCE_PRIORITY,
),



"south korea": create_profile(
    country="South Korea",
    language="ko",
    region="asia",

    construction_terms=[
        "construction",
        "건설",
        "공사",
        "인프라",
        "사업",
    ],

    infrastructure_terms=[
        "도로",
        "교량",
        "교통",
        "도시개발",
    ],

    procurement_terms=[
        "입찰",
        "계약",
        "조달",
    ],

    government_terms=[
        "정부",
        "시청",
        "구청",
        "기관",
    ],

    official_source_terms=[
        "국토교통부",
        "Ministry of Land Infrastructure and Transport",
        "시청",
        "지방자치단체",
    ],

    government_domains=[
        ".go.kr",
    ],

    news_terms=[
        "뉴스",
        "신문",
    ],

    negative_terms=[
        "영화",
        "게임",
        "은행",
        "부동산",
    ],

    search_intents=DEFAULT_SEARCH_INTENTS,

    source_priority=DEFAULT_SOURCE_PRIORITY,
),



"china": create_profile(
    country="China",
    language="zh",
    region="asia",

    construction_terms=[
        "construction",
        "建设",
        "工程",
        "基础设施",
        "项目",
    ],

    infrastructure_terms=[
        "道路",
        "公路",
        "桥梁",
        "交通",
        "城市建设",
    ],

    procurement_terms=[
        "招标",
        "合同",
        "采购",
        "投标",
    ],

    government_terms=[
        "政府",
        "市政府",
        "委员会",
        "部门",
    ],

    official_source_terms=[
        "住房和城乡建设部",
        "交通运输部",
        "地方政府",
        "市政府",
    ],

    government_domains=[
        ".gov.cn",
    ],

    news_terms=[
        "新闻",
        "报道",
    ],

    negative_terms=[
        "电影",
        "游戏",
        "银行",
        "房地产",
    ],

    search_intents=DEFAULT_SEARCH_INTENTS,

    source_priority=DEFAULT_SOURCE_PRIORITY,
),

    "indonesia": create_profile(

        country="Indonesia",

        language="id",

        region="southeast asia",

        construction_terms=[

            "pembangunan",

            "konstruksi",

            "proyek",

            "infrastruktur",

        ],

        infrastructure_terms=[

            "jalan",

            "jembatan",

            "transportasi",

            "pelebaran jalan",

            "perbaikan jalan",

        ],

        procurement_terms=[

            "lelang",

            "pengadaan",

            "kontrak",

            "tender",

        ],

        government_terms=[

            "pemerintah",

            "kementerian",

            "dinas",

            "kabupaten",

            "kota",

        ],

        official_source_terms=[

            "PUPR",

            "Kementerian Pekerjaan Umum",

            "Dinas Pekerjaan Umum",

            "Pemerintah Daerah",

            "Bappeda",

        ],

        government_domains=[

            ".go.id",

        ],

        news_terms=[

            "berita",

            "koran",

            "media",

        ],

        negative_terms=[

            "film",

            "game",

            "bank",

            "rumah",

            "properti",

        ],

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),



    "romania": create_profile(

        country="Romania",

        language="ro",

        region="europe",

        construction_terms=[

            "construcție",

            "lucrări",

            "infrastructură",

            "proiect",

            "dezvoltare",

        ],

        infrastructure_terms=[

            "drum",

            "șosea",

            "pod",

            "modernizare",

            "reabilitare",

            "transport",

        ],

        procurement_terms=[

            "licitație",

            "achiziție",

            "contract",

            "atribuire",

            "procedură",

        ],

        government_terms=[

            "guvern",

            "primărie",

            "consiliu local",

            "minister",

        ],

        official_source_terms=[

            "Primăria",

            "Ministerul Transporturilor",

            "CNAIR",

            "Consiliul Județean",

        ],

        government_domains=[

            ".gov.ro",

            ".ro",

        ],

        news_terms=[

            "știri",

            "ziar",

            "presă",

        ],

        negative_terms=[

            "film",

            "bancă",

            "imobil",

            "joc",

        ],

        search_intents=DEFAULT_SEARCH_INTENTS,

        source_priority=DEFAULT_SOURCE_PRIORITY,

    ),

}