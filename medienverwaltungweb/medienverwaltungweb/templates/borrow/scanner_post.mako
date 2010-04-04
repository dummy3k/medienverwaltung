<%inherit file="/layout-default.mako"/>\

<%def name="title()">${_("What should i do with these?")}</%def>

<%def name="content()">
% if c.available:
<h2>${_("Available Media")}</h2>
<form method="post" action="${h.url_for(controller='borrow', action='checkout_post')}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>&nbsp;</td>
        <td class='simple'>${_('Medium')}</td>
    </tr>
    % for item in c.available:
    <tr>
        <td class='simple'>
            <input type='checkbox' name='item_id_${item.id}' value='${item.id}' checked="checked"/>
        </td>
        <td class='simple'>
            <a href="${h.url_for(controller='medium', action='edit', id=item.id, page=None)}">
                ${item.title}
            </a>
        </td>
    </tr>
    % endfor
</table>
<p>
    ${_("Borrower")}:
    <select name="borrower">
        <option value="-1">${_("Please select one")}</option>
        % for item in c.borrowers:
        <option value="${item.id}">${item.first_name} ${item.last_name}</option>
        % endfor
    </select>
    <input type="submit" value="${_("Checkout marked media")}"/>
</p>
</form>
% endif

% if c.borrowed:
<h2>${_("Return Media")}</h2>
<form method="post" action="${h.url_for(controller='borrow', action='checkin_post')}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>&nbsp;</td>
        <td class='simple'>${_('Borrower')}</td>
        <td class='simple'>${_('Medium')}</td>
        <td class='simple'>${_('Checkout Date')}</td>
    </tr>
    % for item in c.borrowed:
    <tr>
        <td class='simple'>
            <input type='checkbox' name='item_id_${item.id}' value='${item.id}' checked="checked"/>
        </td>
        <td class='simple'>
            <a href="${h.url_for(action='edit_borrower', id=item.borrower.id, page=None)}">
                ${item.borrower.first_name}
                ${item.borrower.last_name}
            </a>
        </td>
        <td class='simple'>
            <a href="${h.url_for(controller='medium', action='edit', id=item.medium.id, page=None)}">
                ${item.medium.title}
            </a>
        </td>
        <td class='simple'>${item.borrowed_ts}</td>
    </tr>
    % endfor
</table>
<p><input type="submit" value="${_("Checkin marked media")}"/></p>
</form>
% endif

</%def>
