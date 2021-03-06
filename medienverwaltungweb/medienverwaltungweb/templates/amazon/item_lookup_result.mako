<%inherit file="/layout-default.mako"/>\

<%def name="title()">${_("Amazon Item Lookup Results")}</%def>

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
    %if 'Actor' in dir(c.item.ItemAttributes):
    <tr>
        <td class='simple'>${_('Actors')}</td>
        <td class='simple'><ul>
        %for subitem in c.item.ItemAttributes.Actor:
        <li>${subitem}</li>
        %endfor
        </ul></td>
    </tr>
    %endif
    <tr>
        <td class='simple'>${_('Images')}</td>
        <td class='simple'>
        % if 'SmallImage' in c.item.__dict__:
        <img src="${unicode(c.item.SmallImage.URL)}" />
        % endif
        % if 'MediumImage' in c.item.__dict__:
        <img src="${unicode(c.item.MediumImage.URL)}" />
        % endif
        % if 'LargeImage' in c.item.__dict__:
        <img src="${unicode(c.item.LargeImage.URL)}" />
        % endif
        </td>
    </tr>
</table>
</%def>


<%def name="side()">
	<div class="box">
    <h2>${_("Actions")}:</h2>
    <ul>
        <li><a href="${c.item.DetailPageURL}">${_("Show Amazon Page")}</a></li>
    </ul>
    </span>
	</div>
</%def>
