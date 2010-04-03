##<%def name="link_to_borrower(item, h)" filter="n">
<%def name="link_to_borrower(item, h)">
<a href="${h.url_for(controller='borrow', action='edit_borrower', id=item.id)}">
    ${item.first_name} ${item.last_name}
</a>
</%def>
