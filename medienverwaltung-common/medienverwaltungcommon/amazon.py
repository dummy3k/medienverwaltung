import logging
import model

log = logging.getLogger(__name__)

class RefHelper():
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return self.value
        
def add_persons(item, relation_name, medium_id, msg, session):
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

    for subitem in item.ItemAttributes.__dict__[relation_name]:
        #~ subitem = str(subitem).encode('utf-8')
        subitem = unicode(subitem)
        log.debug("AUTHOR: %s" % subitem)
        #~ subitem = ("%s" % subitem).encode('utf-8')
        query = session.query(model.Person)
        actor = query.filter(model.Person.name==subitem).first()
        if not actor:
            log.info("new actor: %s" % subitem)
            actor = model.Person()
            actor.name = subitem
            log.debug("Actor.name, bf commit: %s" % actor.name)
            session.add(actor)
            session.commit()
            log.debug("Actor.name, after cm: %s" % actor.name)
            #~ h.flash("added: %s" % actor)
            #~ msg.value += u"%s, " % unicode(actor.name, errors='replace')
            msg.value += u"%s, " % actor.name
            #~ msg.value += u"%s, " % subitem
        log.debug("!!!!!! Actor: %s" % actor)


        query = session.query(model.PersonToMedia)
        record = query.filter(model.PersonToMedia.person_id==actor.id)\
                      .filter(model.PersonToMedia.medium_id==medium_id).first()
        if record:
            log.info("!!!!!!! %s already exists" % record)
        else:
            record = model.PersonToMedia()
            record.person_id = actor.id
            record.medium_id = medium_id
            record.type_id = actor_relation.id
            session.add(record)
            #~ h.flash("added: %s" % record)
