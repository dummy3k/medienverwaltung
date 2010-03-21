<%inherit file="/layout-default.mako"/>\

<%def name="title()">Results</%def>

<%def name="content()">
Query = ${c.query}

<div class='simple'>
<table border=1 class='simple'>
    <tr>
        <td class='simple'>${_('ASIN')}</td>
        <td class='simple'>${_('Title')}</td>
        <td class='simple'>${_('Image')}</td>
    </tr>

    % for item in c.items:
    <tr>
        <td class='simple'>${item.ASIN}</td>
        <td class='simple'>${unicode(item.ItemAttributes.Title)}</td>
        <td class='simple'><img src="${unicode(item.SmallImage.URL)}" /></td>
    </tr>
    %endfor
</table>
</div>
</%def>
