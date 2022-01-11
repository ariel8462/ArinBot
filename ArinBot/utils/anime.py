import re

url = 'https://graphql.anilist.co'

CLEANR = re.compile('<.*?>') 

def clean_html(raw_html: str) -> str:
    """Removes all html tags from the string"""
    clean_text = re.sub(CLEANR, '', raw_html)
    return clean_text

anime_query = """
query ($id: Int, $search: String) {
    Media (id: $id, type: ANIME, search: $search) {
        id
        title {
            romaji
            english
            native
        }
        description
        startDate{
            year
        }
        episodes
        season
        format
        status
        duration
        studios{
            nodes{
                name
            }
        }
        averageScore
        genres
        coverImage {
          extraLarge
          color
        }
        bannerImage
    }
}
"""

manga_query = """
query ($id: Int, $search: String) {
  Media(id: $id, type: MANGA, search: $search) {
    id
    title {
      romaji
      english
      native
    }
    description
    startDate {
      year
    }
    chapters
    format
    status
    volumes
    averageScore
    genres
    coverImage {
      extraLarge
      color
    }
    bannerImage
  }
}
"""
