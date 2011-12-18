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
from persons import PersonAlias, person_aliases_table
from media_type import MediaType, media_types_table
from tag import Tag, tags_table
from borrower import Borrower, borrowers_table
from borrower import BorrowAct, borrow_acts_table
from user import User, UserOpenId, user_openids_table, users_table

orm.mapper(MediaToAsin, media_to_asin_table)
orm.mapper(MediaType, media_types_table)
orm.mapper(Tag, tags_table)

orm.mapper(Medium, media_table, properties = {
    'asins' : orm.relation(MediaToAsin, cascade="all, delete, delete-orphan"),
    'type' : orm.relation(MediaType),
    'tags' : orm.relation(Tag, cascade="all, delete, delete-orphan"),
    'persons_to_media' : orm.relation(PersonToMedia, cascade="all, delete, delete-orphan"),
    'acts' : orm.relation(BorrowAct, cascade="all, delete, delete-orphan"),
    })

orm.mapper(PersonToMedia, person_to_media_table, properties = {
    'person' : orm.relation(Person),
    'relation' : orm.relation(RelationType),
    'medium' : orm.relation(Medium),
    })

orm.mapper(BorrowAct, borrow_acts_table, properties = {
    'borrower' : orm.relation(Borrower),
    'medium' : orm.relation(Medium),
    })

orm.mapper(Person, persons_table, properties = {
    'persons_to_media' : orm.relation(PersonToMedia, cascade="all, delete, delete-orphan"),
    'aliases' : orm.relation(PersonAlias, cascade="all, delete, delete-orphan"),
    })

orm.mapper(RelationType, relation_types_table, properties = {
    'persons_to_media' : orm.relation(PersonToMedia, cascade="all, delete, delete-orphan"),
    })

orm.mapper(Borrower, borrowers_table, properties = {
    'acts' : orm.relation(BorrowAct, cascade="all, delete, delete-orphan"),
    })

orm.mapper(PersonAlias, person_aliases_table, properties = {
    'person' : orm.relation(Person),
    })

orm.mapper(UserOpenId, user_openids_table, properties = {
    'user' : orm.relation(User),
    })

orm.mapper(User, users_table, properties = {
    'media' : orm.relation(Medium),
    })

