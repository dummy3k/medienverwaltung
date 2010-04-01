## -*- coding: utf-8 -*-
<%inherit file="/layout-default.mako"/>\

<%def name="title()">${c.title}</%def>

<%def name="content()">
<%namespace name='js_pager' file='../js_pager.mako' />
${js_pager.js_pager(e)}

<p>${c.page.pager(controller='medium', action=c.pager_action)}</p>

<form id="signin-form" method="post" action="${h.url_for(action='delete', page=None)}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>&nbsp;</td>
        <td class='simple'>&nbsp;</td>
        <td class='simple'>${_('Id')}</td>
        <td class='simple'>${_('Title')}</td>
        <td class='simple'>${_('Tags')}</td>
    </tr>

    % for item in c.page.items:
    ##% for item in c.page.items:
    <tr>
        <td class='simple'>
            <input type="checkbox" name="item_id_${item.id}" value="${item.id}">
            <a href="${h.url_for(action='edit', id=item.id, page=None, type=None, tag=None, return_to=h.url_for())}">Edit</a>
        </td>
        <td class='simple'>
            % if item.image_data:
            <img src="${h.url_for(action='image', id=item.id, page=None, type=None, tag=None, return_to=None, width=20, height=20)}">
            % endif
        </td>
        <td class='simple'>${item.id}</td>
        <td class='simple'>${item.title}</td>
        <td class='simple'>
            % for subitem in item.tags:
            <a href="${h.url_for(tag=subitem.name, page=None)}">
                ${subitem.name}
            </a>
            % endfor
        </td>
##        <td class='simple'><a href="${h.url_for(action='add_asin', id=item.ASIN)}">Add this to db</a></td>
    </tr>
    %endfor
</table>

<p>${c.page.pager(controller='medium', action=c.pager_action)}</p>

<p>
<input type="submit" value="Delete marked Media"/>
##<a href="${h.url_for(action='delete', id=None)}">Delete marked Media</a>
</p>
</form>

</%def>
