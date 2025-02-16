import requests

class OMDb_api:
    API_KEY = "1b95df6b"
    URL = "http://www.omdbapi.com/?apikey="


    def request_movie(movie_name):
        """ This function fetches movie details from the OMDb API using the movie title"""
        url_search_movie_by_omdb_id = f"{OMDb_api.URL}{OMDb_api.API_KEY}&s={movie_name}"
        try:
            res_movie = requests.get(url_search_movie_by_omdb_id)
            res_movie.raise_for_status()
            data_movie = res_movie.json()
            if data_movie.get("Response") == "False":
                raise KeyError(f"Didn't find movie {movie_name} in the API")
            return data_movie['Search']
        except requests.exceptions.ConnectionError:
            print("Error: Unable to connect to the API. Please check your internet connection.")
            return None
        except requests.exceptions.Timeout:
            print("Error: The request timed out. Please try again later.")
            return None
        except KeyError as e:
            print(e)
            return None