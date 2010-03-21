<%inherit file="/layout-default.mako"/>\

<%def name="title()">Item Lookup Results</%def>

<%def name="content()">

<table border=1 class='simple'>
    <tr>
        <td class='simple'>${_('ASIN')}</td>
        <td class='simple'>${c.item.ASIN}</td>
    </tr>
    <tr>
        <td class='simple'>${_('Title')}</td>
        <td class='simple'>${c.item.ItemAttributes.Title}</td>
    </tr>
    <tr>
        <td class='simple'>${_('Actors')}</td>
        <td class='simple'><ul>
        %for subitem in c.item.ItemAttributes.Actor:
        <li>${subitem}</li>
        %endfor
        </ul></td>
    </tr>
    <tr>
        <td class='simple'>${_('Images')}</td>
        <td class='simple'>
        <img src="${unicode(c.item.SmallImage.URL)}" />
        <img src="${unicode(c.item.MediumImage.URL)}" />
        <img src="${unicode(c.item.LargeImage.URL)}" />
        </td>
    </tr>
</table>
</%def>
