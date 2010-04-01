<%inherit file="/layout-default.mako"/>\

<%def name="title()">Search Results for '${c.query}'</%def>

<%def name="content()">

% if c.media_page:
<h2>Media</h2>
    <%namespace name='medium' file='../medium/list.mako' />
    ${medium.bare_content(c.media_page, 'list')}
% endif

% if c.persons_result:
<h2>Persons</h2>
    % for item in c.persons_result:
    <a href="${h.url_for(controller='person', action='index', id=item.id, page=None, type=None)}" >
    ${item.name} &sdot;</a>
    % endfor
% endif


</%def>
