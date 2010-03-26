<%inherit file="/layout-default.mako"/>\

<%def name="title()">All Media Gallery</%def>

<%def name="content()">
<p>
<a href="${h.url_for(action='mass_add', id=None, page=None)}">Add Medium</a>
</p>

<p>${c.page.pager(controller='medium', action='list_gallery')}</p>

% for item in c.page.items:
<a href="${h.url_for(controller='medium', action='index', id=item.id, page=None)}">
<img class="plain" src="${h.url_for(action='image', id=item.id, width=100, height=175)}" />
</a>
% endfor

<p>${c.page.pager(controller='medium', action='list_gallery')}</p>

</%def>
