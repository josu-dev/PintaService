# pyright: basic, reportAttributeAccessIssue=false
# source:
# https://sqlalchemy-utils.readthedocs.io/en/latest/_modules/sqlalchemy_utils/types/ts_vector.html
#
# usage from
# https://stackoverflow.com/questions/13361161/sqlalchemy-with-postgresql-and-full-text-search/73999486#73999486
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import TSVECTOR


class TSVectorType(sa.types.TypeDecorator):
    """
    .. note::

        This type is PostgreSQL specific and is not supported by other
        dialects.

    Provides additional functionality for SQLAlchemy PostgreSQL dialect's
    TSVECTOR_ type. This additional functionality includes:

    * Vector concatenation
    * regconfig constructor parameter which is applied to match function if no
      postgresql_regconfig parameter is given
    * Provides extensible base for extensions such as SQLAlchemy-Searchable_

    .. _TSVECTOR:
        https://docs.sqlalchemy.org/en/latest/dialects/postgresql.html#full-text-search

    .. _SQLAlchemy-Searchable:
        https://www.github.com/kvesteri/sqlalchemy-searchable

    ::

        from sqlalchemy_utils import TSVectorType


        class Article(Base):
            __tablename__ = 'user'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.String(100))
            search_vector = sa.Column(TSVectorType)


        # Find all articles whose name matches 'finland'
        session.query(Article).filter(Article.search_vector.match('finland'))


    TSVectorType also supports vector concatenation.

    ::


        class Article(Base):
            __tablename__ = 'user'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.String(100))
            name_vector = sa.Column(TSVectorType)
            content = sa.Column(sa.String)
            content_vector = sa.Column(TSVectorType)

        # Find all articles whose name or content matches 'finland'
        session.query(Article).filter(
            (Article.name_vector | Article.content_vector).match('finland')
        )

    You can configure TSVectorType to use a specific regconfig.
    ::

        class Article(Base):
            __tablename__ = 'user'
            id = sa.Column(sa.Integer, primary_key=True)
            name = sa.Column(sa.String(100))
            search_vector = sa.Column(
                TSVectorType(regconfig='pg_catalog.simple')
            )


    Now expression such as::


        Article.search_vector.match('finland')


    Would be equivalent to SQL::


        search_vector @@ to_tsquery('pg_catalog.simple', 'finland')

    """

    impl = TSVECTOR
    cache_ok = True

    class comparator_factory(TSVECTOR.Comparator):
        def match(self, other, **kwargs):
            if "postgresql_regconfig" not in kwargs:
                if "regconfig" in self.type.options:
                    kwargs["postgresql_regconfig"] = self.type.options[
                        "regconfig"
                    ]
            return TSVECTOR.Comparator.match(self, other, **kwargs)

        def __or__(self, other):
            return self.op("||")(other)

    def __init__(self, *args, **kwargs):
        """
        Initializes new TSVectorType

        :param *args: list of column names
        :param **kwargs: various other options for this TSVectorType
        """
        self.columns = args
        self.options = kwargs
        super().__init__()


"""
Must execute this command in postgresql:

CREATE EXTENSION unaccent; -- still required it plugs into FTS.

CREATE TEXT SEARCH CONFIGURATION argentino ( COPY = simple );
ALTER TEXT SEARCH CONFIGURATION argentino
  ALTER MAPPING FOR hword, hword_part, word
  WITH unaccent, simple;

from stackexchange:
https://dba.stackexchange.com/questions/177020/creating-a-case-insensitive-and-accent-diacritics-insensitive-search-on-a-field
"""
