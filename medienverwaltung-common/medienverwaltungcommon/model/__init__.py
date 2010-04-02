"""The application's model objects"""
import sqlalchemy as sa
from sqlalchemy import orm

#~ from medienverwaltungweb.model import meta
import meta
from medium import Medium, media_table
from persons import Person, persons_table
from persons import RelationType, relation_types_table
from persons import MediaToAsin, media_to_asin_table
from persons import PersonToMedia, person_to_media_table
from media_type import MediaType, media_types_table
from tag import Tag, tags_table
from borrower import Borrower, borrowers_table

orm.mapper(RelationType, relation_types_table)
orm.mapper(Person, persons_table)
orm.mapper(MediaToAsin, media_to_asin_table)
orm.mapper(MediaType, media_types_table)
orm.mapper(Tag, tags_table)
orm.mapper(Borrower, borrowers_table)

orm.mapper(Medium, media_table, properties = {
    'asins' : orm.relation(MediaToAsin),
    'type' : orm.relation(MediaType),
    'tags' : orm.relation(Tag),
    })

orm.mapper(PersonToMedia, person_to_media_table, properties = {
    'person' : orm.relation(Person),
    'relation' : orm.relation(RelationType),
    })

