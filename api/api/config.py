from dataclasses import dataclass

from environs import Env


@dataclass
class DjangoConfig:
    sekret_key: str


@dataclass
class DBConfig:
    name: str
    engine: str
    user: str
    password: str
    host: str
    port: int


@dataclass
class Config:
    django: DjangoConfig
    db: DBConfig


def load_config(path: str = None):
    env = Env()
    env.read_env(path)

    return Config(
        django=DjangoConfig(
            sekret_key=env.str('SECRET_KEY')
        ),
        db=DBConfig(
            name=env.str('POSTGRES_DB'),
            engine=env.str('POSTGRES_ENGINE'),
            user=env.str('POSTGRES_USER'),
            password=env.str('POSTGRES_PASSWORD'),
            host=env.str('POSTGRES_HOST'),
            port=env.int('POSTGRES_PORT')
        )
    )
