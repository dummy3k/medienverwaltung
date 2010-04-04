<%def name="link_to_person(item, h)">\
<a href="${h.url_for(controller='person', action='edit', id=item.id)}">${item.name} (${len(item.persons_to_media)})</a></%def>
