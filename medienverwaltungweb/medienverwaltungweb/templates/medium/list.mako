## -*- coding: utf-8 -*-
<%inherit file="/layout-default.mako"/>\
<%namespace name='medium_block' file='medium_block.mako' />
<%namespace name='js_pager' file='../js_pager.mako' />

<%def name="title()">${c.title}</%def>

<%def name="content()">
${js_pager.js_pager(e)}
${self.bare_content(c.page, c.pager_action)}
</%def>

<%def name="bare_content(pager, pager_action)">

${_("Sort by")}:
<a href="${h.url_for(controller='medium', action='list', order=h.iif(c.order=='created_ts', 'created_ts_desc', 'created_ts'))}">${_('created_ts')}</a>
 &sdot; <a href="${h.url_for(controller='medium', action='list', order=h.iif(c.order=='updated_ts', 'updated_ts_desc', 'updated_ts'))}">${_('updated_ts')}</a>

<p>${pager.pager(controller='medium', action=pager_action, order=request.params.get('order'))}</p>

<form method="post" action="${h.url_for(controller='medium', action='delete', page=None)}">
<table border=1 class='simple'>
    <tr>
        <td class='simple'>&nbsp;</td>
        <td class='simple'><a href="${h.url_for(controller='medium', action='list', order=h.iif(c.order=='id', 'id_desc', 'id'))}">${_('Id')}</a></td>
        <td class='simple'><a href="${h.url_for(controller='medium', action='list', order=h.iif(c.order=='title', 'title_desc', 'title'))}">${_('Title')}</a></td>
    </tr>

    % for item in pager.items:
    <tr>
        <td class='simple'>
            <input type="checkbox" name="item_id_${item.id}" value="${item.id}">
        </td>
        <td class='simple'>${item.id}</td>
        <td class='simple' width="100%">
        ${medium_block.medium_block(item)}
        </td>
    </tr>
    %endfor
</table>

<p>${pager.pager(controller='medium', action=pager_action)}</p>

<p>
<p><input type="submit" value="${_("Delete marked Media")}" class="button"/></p>
##<a href="${h.url_for(action='delete', id=None)}">${_("Delete marked Media")}</a>
</p>
</form>

</%def>

<%def name="side()">
	<div class="box">
        <h2>${_("List")}:</h2>
        <ul>
        <li><a href="${h.url_for(controller='medium', action='list_gallery', id=None, page=None)}">${_("As Gallery")}</a></li>
        </ul>
	</div>
    % if c.tags:
	<div class="box">
        <h2>${_("Tags")}:</h2>
        <span class="tags">
        % for item in c.tags[:10]:
        <a href="${h.url_for(controller='medium', action='list', tag=item[0], page=None)}">${item[0]}&nbsp;(${item[1]})</a>
        % endfor
        </span>
	</div>
    % endif
</%def>
