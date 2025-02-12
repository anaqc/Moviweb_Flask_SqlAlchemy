from abc import ABC, abstractmethod


class DataMangerInterface(ABC):
    
    
    @abstractmethod
    def get_all_users(self):
        ...
    

    @abstractmethod
    def get_user_movies(self):
        ...


    @abstractmethod
    def get_all_movies(self):
        ...

