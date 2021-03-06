import logging
import model

log = logging.getLogger(__name__)

class RefHelper():
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value

def find(haystack, condition):
    for x in haystack:
        if condition(x):
            return x

    raise KeyError("condition did not match")

        
def add_persons(item, relation_name, medium, added_persons, session):
    if not relation_name in item.ItemAttributes.__dict__:
        log.warn("asin %s has no '%s'" % (item.ASIN, relation_name))
        return

    query = session.query(model.RelationType)
    actor_relation = query.filter(model.RelationType.name==relation_name).first()
    if not actor_relation:
        actor_relation = model.RelationType()
        actor_relation.name = relation_name
        session.add(actor_relation)
        log.info("created %s" % actor_relation)
        #~ abort(404)
        
    log.debug("actor_relation: %s" % actor_relation)
    #~ medium = session.query(model.Medium).get(medium_id)

    for subitem in item.ItemAttributes.__dict__[relation_name]:
        subitem = unicode(subitem)
        log.debug("amazon person: %s" % subitem)
        alias = session.query(model.PersonAlias)\
                       .filter(model.PersonAlias.name==subitem)\
                       .first()
        if alias:
            log.debug("found alias '%s' -> '%s'" % (alias.name, alias.person.name))
            actor = alias.person
        else:
            query = session.query(model.Person)
            actor = query.filter(model.Person.name==subitem).first()

        if not actor:
            log.info("new actor: %s" % subitem)
            actor = model.Person()
            actor.name = subitem
            #log.debug("Actor.name, bf commit: %s" % actor)
            session.add(actor)
            session.commit()
            #log.debug("Actor.name, after cm: %s" % actor)

        #~ query = session.query(model.PersonToMedia)
        #~ record = query.filter(model.PersonToMedia.person_id==actor.id)\
                      #~ .filter(model.PersonToMedia.medium_id==medium.id).first()

        try:
            record = find(medium.persons_to_media, lambda item: item.person_id==actor.id and item.medium_id==medium.id)
        except KeyError:
            record = None

        if record:
            log.info("!!!!!!! %s already exists" % record)
        else:
            record = model.PersonToMedia()
            record.person_id = actor.id
            record.type_id = actor_relation.id
            medium.persons_to_media.append(record)

            added_persons.append(actor)
