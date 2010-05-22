## -*- coding: utf-8 -*-
<%inherit file="/layout-default.mako"/>\
<%namespace name='js_pager' file='../js_pager.mako' />

<%def name="title()">${c.title}</%def>

<%def name="content()">
${js_pager.js_pager(e)}

<p>${c.page.pager(role=request.params.get('role'))}</p>

<form id="signin-form" method="post" action="${h.url_for(controller='person', action='delete', page=None)}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>&nbsp;</td>
        <td class='simple'>${_('Id')}</td>
        <td class='simple'>${_('Name')}</td>
    </tr>

    ##% for item in c.page.items:
    % for item in c.page.items:
    <tr>
        <td class='simple'>
##            <input type="checkbox" name="item_id_${item.id}" value="${item.id}">
            <a href="${h.url_for(controller='person', action='edit', id=item.id, page=None)}">${_("Edit")}</a>
        </td>
        <td class='simple'>${item.id}</td>
        <td class='simple'>${item.name}</td>
    </tr>
    %endfor
</table>

<p>
<p>${c.page.pager(role=request.params.get('role'))}</p>
<input type="submit" value='${_("Delete marked Media")}' class="button"/>
</p>
</form>
</%def>


<%def name="side()">
	<div class="box">
        <h2>${_("Filter")}:</h2>
        <ul>
        <li><a href="${h.url_for(controller='person', action='list', role='Actor', page=None)}">${_("Actors")}</a></li>
        <li><a href="${h.url_for(controller='person', action='list', role='Director', page=None)}">${_("Directors")}</a></li>
        </ul>
	</div>
</%def>
