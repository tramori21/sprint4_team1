from etl.genres_etl import run as genres_run
from etl.persons_etl import run as persons_run
from etl.movies_etl import run as movies_run


def main():
    genres_run()
    persons_run()
    movies_run()


if __name__ == "__main__":
    main()
