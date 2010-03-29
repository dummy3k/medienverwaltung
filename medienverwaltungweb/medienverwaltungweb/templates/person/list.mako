## -*- coding: utf-8 -*-
<%inherit file="/layout-default.mako"/>\

<%def name="title()">All Persons</%def>

<%def name="content()">
<p>${c.page.pager()}</p>

<form id="signin-form" method="post" action="${h.url_for(action='delete', page=None)}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>&nbsp;</td>
        <td class='simple'>${_('Id')}</td>
        <td class='simple'>${_('Name')}</td>
##        <td class='simple'>${_('Actions')}</td>
    </tr>

    ##% for item in c.page.items:
    % for item in c.page.items:
    <tr>
        <td class='simple'>
##            <input type="checkbox" name="item_id_${item.id}" value="${item.id}">
            <a href="${h.url_for(action='edit', id=item.id, page=None)}">Edit</a>
        </td>
        <td class='simple'>${item.id}</td>
        <td class='simple'>${item.name}</td>
##        <td class='simple'><a href="${h.url_for(action='add_asin', id=item.ASIN)}">Add this to db</a></td>
    </tr>
    %endfor
</table>

<p>
<p>${c.page.pager()}</p>
<input type="submit" value="Delete marked Media"/>
</p>
</form>

</%def>


<%def name="side()">
	<div class="box">
        <h2>Filter:</h2>
        <ul>
        <li><a href="${h.url_for(role='Actor')}">Actor</a></li>
        <li><a href="${h.url_for(role='Director')}">Director</a></li>
        </ul>
	</div>
</%def>
