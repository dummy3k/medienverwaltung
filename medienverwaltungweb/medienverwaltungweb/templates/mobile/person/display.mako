<%inherit file="/layout-mobile.mako"/>\
<%namespace name='person_snippets' file='/person/snippets.mako' />
<%namespace name='medium_block' file='/medium/medium_block.mako' />

<%def name="title()">${_("Edit Person - '%s'") % c.item.name}</%def>

<%def name="content()">

<h1>${c.item.name}</h1>

<p>${c.page.pager()}</p>
% for item in c.page.items:
<div>
##    
##    <span class='field_value'>${c.item.id}</span>
    ##<td class='simple'>${_(item.relation.name)}</td>
    ##<span class='field_name'>${_('Id')}</span>
    ##<span class='field_name'>${_('Id')}</span>
    ##<td class='simple' width="100%">
        ${medium_block.medium_block(item.medium)}
</div>
% endfor

<p>${c.page.pager()}</p>

####<SCRIPT language="JavaScript">
####<!--
####document.write("width: " + window.innerWidth + "<br>");
####document.write("height: " + window.innerHeight + "<br>");
####//-->
####</SCRIPT>


##% if c.item.image_data and True:
##<div style="float:right">
####<p>
##    <a href="${h.url_for(controller='image', action='raw_image', id=c.item.id)}">
##    <img src="${h.url_for(controller='image', action='thumbnail', id=c.item.id, width=100, height=300)}" class="plain"/>
##    </a>
####</p>
##</div>
##% endif

##% if c.borrowed_by:
##<p>
##${_("This medium ist currently borrowed to %s.") % h.tmpl('borrow/snippets.mako', 'link_to_borrower').render_unicode(item=c.borrowed_by, h=h) |n}
##</p>
##% endif

##% if len(c.item.tags) > 0:
##<div>
##    <span class='field_name'>${_('Tags')}</span>
##    <span class='field_value'>${c.item.get_tagstring()}</span>
##</div>
##% endif
##% if c.item.isbn:
##<div>
##    <span class='field_name'>${_('ISBN')}</span>
##    <span class='field_value'>${c.item.isbn}</span>
##</div>
##% endif
##%for subitem in c.persons:
##<div>
##    <span class='field_name'>${_(subitem)}</span>
##    <span class='field_value'>
##    % for subsubitem in c.persons[subitem]:
##    ${person_snippets.link_to_person(subsubitem.person, h)}, 
##    % endfor
##    </span>
##</div>
##% endfor
##<div>
##    <span class='field_name'>${_('Created')}</span>
##    <span class='field_value'>${h.strftime(c.item.created_ts)}</span>
##</div>
##<div>
##    <span class='field_name'>${_('Updated')}</span>
##    <span class='field_value'>${h.strftime(c.item.updated_ts)}</span>
##</div>

##<form id="mainform" method="post" action="${h.url_for(controller='medium', action='edit_post')}">
####<input type="hidden" name="id" value="${c.item.id}" />
####<input type="hidden" name="return_to" value="${request.params.get('return_to')}"/>
####<p><input type="submit" value="${_('Save')}" class="button"/></p>
##</form>

</%def>
