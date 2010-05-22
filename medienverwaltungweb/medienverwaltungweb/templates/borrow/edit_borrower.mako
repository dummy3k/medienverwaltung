<%inherit file="/layout-default.mako"/>\
<%namespace name='medium_block' file='../medium/medium_block.mako' />

<%def name="title()">${_("Edit Borrower - '%s %s'") % (c.item.first_name, c.item.last_name)}</%def>

<%def name="content()">
<h2>${_("Borrower Details")}</h2>
<form id="signin-form" method="post" action="${h.url_for(controller='borrow', action='edit_borrower_post')}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'><nobr>${_('First Name')}</nobr></td>
        <td class='simple'><input type="text" name="first_name" value="${c.item.first_name}" size=50 /></td>
    </tr>
    <tr>
        <td class='simple'><nobr>${_('Last Name')}</nobr></td>
        <td class='simple'><input type="text" name="last_name" value="${c.item.last_name}" size=50 /></td>
    </tr>
    <tr>
        <td class='simple'><nobr>${_('eMail')}</nobr></td>
        <td class='simple'><input type="text" name="email" value="${c.item.email}" size=50 /></td>
    </tr>
</table>
<p>
##<input type="hidden" name="return_to" value="${request.params.get('return_to')}"/>
<input type="submit" value="${_("Save")}" class="button"/>
</p>
</form>

% if c.borrowed_media:
<h2>${_("Borrowed Items")}</h2>
<form id="signin-form" method="post" action="${h.url_for(controller='borrow', action='checkin_post')}">
<table>
% for item in c.borrowed_media:
    <tr>
        <td>
            <input type="checkbox" name="item_id_${item.id}" value="${item.id}">
        <td>
        <td>
            ${medium_block.medium_block(item.medium)}
        <td>
    </tr>
% endfor
</table>
<input type="submit" value="${_("Checkin")}" class="button"/>
</form>
% endif

</%def>


<%def name="side()">
	<div class="box">
        <h2>${_("Actions")}:</h2>
        <ul>
            <li><a href="${h.url_for(controller='borrow', action='show_history')}">${_("Borrow History")}</a></li>
            <li><a href="${h.url_for(controller='borrow', action='add_borrower', id=None)}">${_("Add Borrower")}</a></li>
            <li><a style="cursor:pointer" onclick="if (confirm('${_("Really delete this borrower?")}')) {location.href = '${h.url_for(controller='borrow', action='delete_borrower_post')}';}">${_("Delete '%s %s'") % (c.item.first_name, c.item.last_name)}</a></li>
        </ul>
	</div>
</%def>
