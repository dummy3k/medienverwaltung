## -*- coding: utf-8 -*-
<%inherit file="/layout-default.mako"/>\

<%def name="title()">${c.title}</%def>

<%def name="content()">
<%namespace name='js_pager' file='../js_pager.mako' />
${js_pager.js_pager(e)}

<p>${c.page.pager()}</p>

<form id="signin-form" method="post" action="${h.url_for(action='delete', page=None)}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>${_('Borrower')}</td>
        <td class='simple'>${_('Medium')}</td>
        <td class='simple'>${_('Checkout Date')}</td>
        <td class='simple'>${_('Checkin Date')}</td>
    </tr>
    % for item in c.page.items:
    <tr>
        <td class='simple'>
            <a href="${h.url_for(action='edit_borrower', id=item.borrower.id, page=None)}">
                ${item.borrower.first_name}
                ${item.borrower.last_name}
            </a>
        </td>
        <td class='simple'>
            <a href="${h.url_for(action='edit', id=item.medium.id, page=None)}">
                ${item.medium.title}
            </a>
        </td>
        <td class='simple'>${item.borrowed_ts}</td>
        <td class='simple'>${item.returned_ts}</td>
    </tr>
    %endfor
</table>

<p>${c.page.pager()}</p>
</form>

</%def>

<%def name="side()">
	<div class="box">
        <h2>Actions:</h2>
        <ul>
            <li><a href="${h.url_for(controller='borrow', action='add_borrower', id=None)}">Add Borrower</a></li>
        </ul>
	</div>
</%def>
