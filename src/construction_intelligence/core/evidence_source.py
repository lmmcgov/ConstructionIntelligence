"""
Evidence source definitions.

EvidenceSource describes where supporting information about a project
was obtained.
"""

from enum import Enum


class EvidenceSource(str, Enum):
    """
    Origin of project evidence.

    This is separate from ProjectOrigin:
    - ProjectOrigin = where the project record came from
    - EvidenceSource = where supporting information came from
    """

    #
    # Mapping / structured geospatial sources
    #
    OSM = "osm"

    #
    # Official public-sector sources
    #
    GOVERNMENT_RECORD = "government_record"

    GOVERNMENT_WEBSITE = "government_website"

    CITY_PROJECT_PAGE = "city_project_page"

    PLANNING_DOCUMENT = "planning_document"

    PROCUREMENT = "procurement"

    PERMIT = "permit"

    #
    # Private-sector sources
    #
    CONTRACTOR_NOTICE = "contractor_notice"

    DEVELOPER_NOTICE = "developer_notice"

    #
    # Public reporting sources
    #
    NEWS_ARTICLE = "news_article"

    #
    # Generic web sources
    #
    OTHER_WEB = "other_web"