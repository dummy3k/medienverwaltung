<%inherit file="/layout-default.mako"/>\
<%namespace name='medium_block' file='/medium/medium_block.mako' />
<%namespace name='person_snippets' file='/person/snippets.mako' />

<%def name="title()">${_("Search Results for '%s'") % c.query}'</%def>

<%def name="content()">

<div class="contentbox">
% if c.media_page:
<h2>${_("Media")}</h2>
% for item in c.media_page:
${medium_block.medium_block(item)}
% endfor
% endif
</div>

<div class="contentbox">
% if c.persons_result:
<h2>${_("Persons")}</h2>
<ul>
    % for item in c.persons_result:
    <li>
##        <a href="${h.url_for(controller='person', action='index', id=item.id, page=None, type=None)}" >
##        ${item.name} &sdot;</a>
        ${person_snippets.link_to_person(item, h)}
    </li>
    % endfor
<ul>
% endif
</div>


</%def>
