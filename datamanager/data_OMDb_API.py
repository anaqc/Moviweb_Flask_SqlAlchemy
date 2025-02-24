import requests

class OMDb_api:
    API_KEY = "1b95df6b"
    URL = "http://www.omdbapi.com/?apikey="


    def request_movie_search(movie_name):
        """ This function fetches movie details from the OMDb API using the movie title"""
        url_search_movie_by_name = f"{OMDb_api.URL}{OMDb_api.API_KEY}&s={movie_name}"
        try:
            res_movie = requests.get(url_search_movie_by_name)
            res_movie.raise_for_status()
            data_movie = res_movie.json()
            if data_movie.get("Response") == "False":
                raise KeyError(f"Didn't find movie {movie_name} in the API")
            return OMDb_api._filter_request_movie_data(data_movie['Search'])
        except requests.exceptions.ConnectionError:
            print("Error: Unable to connect to the API. Please check your internet connection.")
            return None
        except requests.exceptions.Timeout:
            print("Error: The request timed out. Please try again later.")
            return None
        except KeyError as e:
            print(e)
            return None
        

    def _request_movie_by_id(imdb_id):
        """ This function fetches the movie details form the OMDb API using the imdbID"""
        url_search_movie_by_imdb_id = f"{OMDb_api.URL}{OMDb_api.API_KEY}&i={imdb_id}"
        try:
            res_movie = requests.get(url_search_movie_by_imdb_id)
            res_movie.raise_for_status()
            movie_details = res_movie.json() 
            if movie_details.get("Response") == "False":
                raise KeyError(f"Didn't find movie in the API")
            return movie_details
        except requests.exceptions.ConnectionError:
            print("Error: Unable to connect to the API. Please check your internet connection.")
            return None
        except requests.exceptions.Timeout:
            print("Error: The request timed out. Please try again later.")
            return None
        except KeyError as e:
            print(e)
            return None
    

    def _filter_request_movie_data(data_movies):
        """ This function filter the data_movies and search the movie by imdbID """
        new_data = []
        for movie in data_movies:
            movie_imdbID = movie.get("imdbID")
            movie_info = OMDb_api._request_movie_by_id(movie_imdbID)
            movie_director = movie_info.get("Director")
            movie_poster = movie_info.get("Poster")
            movie_genre = movie_info.get("Genre")
            movie_type = movie_info.get("Type")
            new_data.append({
                "Title" : movie_info.get("Title"),
                "Director" : movie_director if movie_director != "None" else "",
                "Year" : OMDb_api._get_validate_year(movie_info.get("Year")),
                "imdbRating" : OMDb_api._get_validate_rating(movie_info.get("imdbRating")),
                "Poster" : movie_poster if movie_poster != "None" else "",
                "imdbID" : movie_imdbID if movie_imdbID != "None" else "",
                "Genre" : movie_genre if movie_genre != "None" else "",
                "Type": movie_type if movie_type != "None" else "" 
            })
        return new_data


    @staticmethod          
    def _get_validate_year(year):
        """ This function convert the string year to int"""
        if isinstance(year,str) and len(year) >= 4:
            validate_year = year[:4]
            if validate_year.isdigit():
                return int(validate_year)
        return 0
    

    def _get_validate_rating(rating):
        """ This function convert the string rating to float"""
        try: 
            return float(rating)
        except ValueError:
            return 0
