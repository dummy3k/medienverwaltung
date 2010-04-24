## -*- coding: utf-8 -*-
<%inherit file="/layout-default.mako"/>\
<%namespace name='person_snippets' file='/person/snippets.mako' />

<%def name="title()">${_("Merge Persons")}</%def>

<%def name="content()">

${_("Please select the name you want to be displayed. All other Persons will be merged into this one.")}

<form id="mainform" method="post" action="${h.url_for(action='merge_post', id=None)}">
% for index, item in enumerate(c.persons):
<p>
    % if index == 0:
    <input type="radio" name="primary_id" value="${item.id}" checked="checked" />
    % else:
    <input type="radio" name="primary_id" value="${item.id}" />
    % endif
    
    ${person_snippets.link_to_person(item, h)}
</p>
% endfor
<input type="hidden" name="person_ids_str" value="${c.person_ids_str}" />
<input type="hidden" name="return_to" value="${request.params.get('return_to')}" />
<p><input type="submit" value="${_('Merge')}" class="button"/></p>
</form>

##c.person_id_str: ${c.person_ids_str}
##foo: ${",".join(h.checkboxes(request, 'person_id_'))}
</%def>
