<%inherit file="/layout-default.mako"/>\

<%def name="title()">Item Search Results</%def>

<%def name="content()">
Query = ${c.query}

<div class='simple'>
<table border=1 class='simple'>
    <tr>
        <td class='simple'>${_('ASIN')}</td>
        <td class='simple'>${_('Title')}</td>
        <td class='simple'>${_('Image')}</td>
        <td class='simple'>${_('Actions')}</td>
    </tr>

    % for item in c.items:
    <tr>
        <td class='simple'>${item.ASIN}</td>
        <td class='simple'>${unicode(item.ItemAttributes.Title)}</td>
        <td class='simple'><img src="${unicode(item.SmallImage.URL)}" /></td>
        <td class='simple'><a href="${h.url_for(action='add_asin', id=item.ASIN)}">Add this to db</a></td>
    </tr>
    %endfor
</table>
</div>
</%def>
