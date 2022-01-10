url = 'https://graphql.anilist.co'

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
        type
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
        bannerImage
    }
}
"""
