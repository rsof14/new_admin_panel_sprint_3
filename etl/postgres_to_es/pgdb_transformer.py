from pydantic import BaseModel
import datetime


class ElasticPerson(BaseModel):
    id: str
    name: str


class ElasticMovie(BaseModel):
    id: str
    imdb_rating: float
    genre: list[str] = []
    title: str
    description: str
    director: list[str] = []
    actors_names: list[str] = []
    writers_names: list[str] = []
    directors: list[ElasticPerson] = []
    actors: list[ElasticPerson] = []
    writers: list[ElasticPerson] = []


class ElasticTransformer:
    def transform_persons(self, persons):
        director = []
        directors = []
        actors_names = []
        actors = []
        writers_names = []
        writers = []
        for person in persons:
            if person['person_role'] == 'director':
                director.append(person['person_name'])
                directors.append(ElasticPerson(id=person['person_id'], name=person['person_name']))
            if person['person_role'] == 'actor':
                actors_names.append(person['person_name'])
                actors.append(ElasticPerson(id=person['person_id'], name=person['person_name']))
            if person['person_role'] == 'writer':
                writers_names.append(person['person_name'])
                writers.append(ElasticPerson(id=person['person_id'], name=person['person_name']))
        return {'directors_names': director, 'directors': directors, 'actors_names': actors_names,
                'actors': actors, 'writers_names': writers_names, 'writers': writers}

    def transform_data(self, rows):
        movies_data = []
        for row in rows:
            persons_data = self.transform_persons(row['persons'])
            movie_data = ElasticMovie(
                id=row['id'],
                imdb_rating=row['rating'],
                genre=row['genres'],
                title=row['title'],
                description=row['description'],
                director=persons_data['directors_names'],
                actors_names=persons_data['actors_names'],
                writers_names=persons_data['writers_names'],
                directors=persons_data['directors'],
                actors=persons_data['actors'],
                writers=persons_data['writers']
            )
            movies_data.append(movie_data.dict())
        return movies_data
