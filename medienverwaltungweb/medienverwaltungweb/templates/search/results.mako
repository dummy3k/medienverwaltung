<%inherit file="/layout-default.mako"/>\

<%def name="title()">Search</%def>

<%def name="content()">

% if c.media_result:
<h2>Media</h2>
    % for item in c.media_result:
    <a href="${h.url_for(controller='medium', action='index', id=item.id, page=None)}" >
    ${item.title}</a>
    % endfor
% endif

% if c.persons_result:
<h2>Persons</h2>
    % for item in c.persons_result:
    <a href="${h.url_for(controller='person', action='index', id=item.id, page=None)}" >
    ${item.name}</a>
    % endfor
% endif


</%def>
