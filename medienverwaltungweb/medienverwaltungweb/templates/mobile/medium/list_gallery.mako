<%inherit file="/layout-mobile.mako"/>\
<%namespace name='person_snippets' file='/person/snippets.mako' />

<%def name="title()">${c.title}</%def>

<%def name="content()">

<h1>${c.title}</h1>

<p>${c.page.pager(controller='medium', action='list_gallery')}</p>

<p>
% for item in c.page.items:
<div class='centered'>
<a href="${h.url_for(controller='medium', action='index', id=item.id, mobile=c.mobile)}">
<img class="plain" src="${h.url_for(controller='image', action='thumbnail', id=item.id, width=150, height=200, type=None, tag=None, page=None)}" />
</a>
</div>
% endfor
</p>

<p>${c.page.pager(controller='medium', action='list_gallery')}</p>

</%def>
