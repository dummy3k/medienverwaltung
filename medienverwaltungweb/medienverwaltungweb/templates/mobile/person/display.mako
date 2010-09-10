<%inherit file="/layout-mobile.mako"/>\
<%namespace name='person_snippets' file='/person/snippets.mako' />
<%namespace name='medium_block' file='/medium/medium_block.mako' />

<%def name="title()">${_("Edit Person - '%s'") % c.item.name}</%def>

<%def name="content()">

<h1>${c.item.name}</h1>

<p>${c.page.pager()}</p>
% for item in c.page.items:
<div>
    ##<td class='simple'>${_(item.relation.name)}</td>
    ${medium_block.medium_block(item.medium)}
</div>
% endfor

<p>${c.page.pager()}</p>
</%def>
