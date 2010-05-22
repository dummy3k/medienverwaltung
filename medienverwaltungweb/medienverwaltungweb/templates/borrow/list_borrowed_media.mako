## -*- coding: utf-8 -*-
<%inherit file="/layout-default.mako"/>\

<%def name="title()">${_("Borrowed Media List")}</%def>

<%def name="content()">

<form method="post" action="${h.url_for(controller='borrow', action='checkin_post')}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>&nbsp;</td>
        <td class='simple'>${_('Borrower')}</td>
        <td class='simple'>${_('Medium')}</td>
        <td class='simple'>${_('Checkout Date')}</td>
    </tr>
    % for item in c.borrow_acts:
    <tr>
        <td class='simple'>
            <input type='checkbox' name='item_id_${item.id}' value='${item.id}' class="button"/>
        </td>
        <td class='simple'>
            <a href="${h.url_for(controller='borrow', action='edit_borrower', id=item.borrower.id, page=None)}">
                ${item.borrower.first_name}
                ${item.borrower.last_name}
            </a>
        </td>
        <td class='simple'>
            <a href="${h.url_for(controller='medium', action='edit', id=item.medium.id, page=None)}">
                ${item.medium.title}
            </a>
        </td>
        <td class='simple'>${h.strftime(item.borrowed_ts)}</td>
    </tr>
    %endfor
</table>
<p><input type="submit" value="${_("Checkin marked media")}" class="button"/></p>
</form>

</%def>

<%def name="side()">
	<div class="box">
        <h2>${_("Actions")}:</h2>
        <ul>
            <li><a href="${h.url_for(controller='borrow', action='add_borrower', id=None)}">${_("Add Borrower")}</a></li>
            <li><a href="${h.url_for(controller='borrow', action='list_borrowers')}">${_("List Borrowers")}</a></li>
            <li><a href="${h.url_for(controller='borrow', action='scanner')}">${_("Barcode Scanner")}</a></li>
        </ul>
	</div>
</%def>
