<%def name="link_to_person(item, h)">\
% if len(item.persons_to_media) > 1:
<a href="${h.url_for(controller='person', action='edit', id=item.id)}">${item.name} (${len(item.persons_to_media)})</a>\
% else:
<a href="${h.url_for(controller='person', action='edit', id=item.id)}">${item.name}</a>\
% endif
</%def>\
