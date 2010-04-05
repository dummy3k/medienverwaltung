## -*- coding: utf-8 -*-
<%inherit file="/layout-default.mako"/>\
<%!
    import urllib
%>
<%namespace name='medium_block' file='/medium/medium_block.mako' />

<%def name="title()">${_("Edit Person - '%s'") % c.item.name}</%def>

<%def name="content()">
<form id="signin-form" method="post" action="${h.url_for(controller='person', action='edit_post', id=None)}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>${_('Id')}</td>
        <td class='simple'>${c.item.id}</td>
    </tr>
    <tr>
        <td class='simple'>${_('Name')}</td>
        <td class='simple'><input type="text" name="title" value="${c.item.name}" /></td>
    </tr>
    <tr>
        <td class='simple'>${_('Aliases')}</td>
        <td class='simple'>
            <ul>
            % for item in c.item.aliases:
            <li>${item.name}</li>
            % endfor
            </ul>
        </td>
    </tr>
</table>
<input type="hidden" name="id" value="${c.item.id}" />
<p><input type="submit" value="${_("Save")}"/></p>
</form>


<h2>${_("Appeared in this media")}</h2>
<p>${c.page.pager()}</p>

<table border=1 class='simple'>
    <tr>
        <td class='simple'>${_('Role')}</td>
        <td class='simple'>${_('Medium')}</td>
    </tr>
    % for item in c.page.items:
    <tr>
        <td class='simple'>${_(item.relation.name)}</td>
        <td class='simple' width="100%">
            ${medium_block.medium_block(item.medium)}
        </td>
    </tr>
    % endfor
</table>
<p>${c.page.pager()}</p>

##<iframe src="http://de.wikipedia.org/wiki/${urllib.quote(c.item.name)}" width="600" height="600" name="SELFHTML_in_a_box">
<iframe src="http://de.wikipedia.org/wiki/${c.item.name}" width="600" height="600" name="SELFHTML_in_a_box">
  <p>no iframe</a></p>
</iframe>

</%def>
