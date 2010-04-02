from sqlalchemy import *
import meta

borrowers_table = Table('borrowers', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', Unicode(50)),
    Column('last_name', Unicode(50)),
    Column('email', Unicode(50)),
    Column('created_ts', DateTime),
    Column('updated_ts', DateTime),
)

borrow_history_table = Table('borrow_history', meta.metadata,
    Column('id', Integer, primary_key=True),
    Column('media_id', Integer, ForeignKey('media.id')),
    Column('borrower_id', Integer, ForeignKey('borrowers.id')),
    Column('borrowed_ts', DateTime),
    Column('returned_ts', DateTime),
)


class Borrower(object):
    def __unicode__(self):
        return self.__repr__()

    __str__ = __unicode__

    def __repr__(self):
        return "<Borrower(%s, '%s %s')>" % (self.id,
                                            self.first_name,
                                            self.last_name)
