<%inherit file="/layout-mobile.mako"/>\
<%namespace name='person_snippets' file='/person/snippets.mako' />
<%namespace name='medium_block' file='/medium/medium_block.mako' />

<%def name="title()">${_("Edit Borrower - '%s %s'") % (c.item.first_name, c.item.last_name)}</%def>

<%def name="content()">

<h1>${c.item.first_name} ${c.item.last_name}</h1>

<div>
    <span class='field_name'>${_('eMail')}</span>
    <span class='field_value'>
        <a href='mailto:${c.item.email}'>
        ${c.item.email}
        </a>
    </span>
</div>

##<p>${c.page.pager()}</p>
##% for item in c.page.items:
##<div>
##    ##<td class='simple'>${_(item.relation.name)}</td>
##    ${medium_block.medium_block(item.medium)}
##</div>
##% endfor
##<p>${c.page.pager()}</p>

</%def>
