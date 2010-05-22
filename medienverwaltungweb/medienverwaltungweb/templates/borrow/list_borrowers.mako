## -*- coding: utf-8 -*-
<%inherit file="/layout-default.mako"/>\

<%def name="title()">${c.title}</%def>

<%def name="content()">
<%namespace name='js_pager' file='../js_pager.mako' />
${js_pager.js_pager(e)}

<p>${c.page.pager()}</p>

<form id="signin-form" method="post" action="${h.url_for(controller='borrow', action='delete', page=None)}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>&nbsp;</td>
        <td class='simple'>${_('Id')}</td>
        <td class='simple'>${_('First Name')}</td>
        <td class='simple'>${_('Last Name')}</td>
        <td class='simple'>${_('eMail')}</td>
    </tr>
    % for item in c.page.items:
    <tr>
        <td class='simple'>
            <a href="${h.url_for(controller='borrow', action='edit_borrower', id=item.id, page=None)}">${_("Edit")}</a>
        </td>
        <td class='simple'>${item.id}</td>
        <td class='simple'>${item.first_name}</td>
        <td class='simple'>${item.last_name}</td>
        <td class='simple'>${item.email}</td>
    </tr>
    %endfor
</table>

<p>${c.page.pager()}</p>
##<p>
##<input type="submit" value="Delete marked Media"/>
##</p>
</form>

</%def>

<%def name="side()">
	<div class="box">
        <h2>${_("Actions")}:</h2>
        <ul>
            <li><a href="${h.url_for(controller='borrow', action='add_borrower', id=None)}">${_("Add Borrower")}</a></li>
        </ul>
	</div>
</%def>
