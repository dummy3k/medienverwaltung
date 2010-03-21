Query = ${c.query}


<table border=1>
    <tr>
        <td>${_('ASIN')}</td>
        <td>${_('Title')}</td>
        <td>${_('Image')}</td>
    </tr>

    % for item in c.items:
    <tr>
        <td>${item.ASIN}</td>
        <td>${unicode(item.ItemAttributes.Title)}</td>
        <td><img src="${unicode(item.SmallImage.URL)}" /></td>
    </tr>
    %endfor
</table>
