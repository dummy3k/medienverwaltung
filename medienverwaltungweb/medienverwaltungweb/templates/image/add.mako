<%inherit file="/layout-default.mako"/>\

<%def name="title()">${_("Add Image to Media")}</%def>

<%def name="content()">
<form id="signin-form" method="post" action="${h.url_for(action='mass_add_post')}">
    <p>${_("Type")}:
        % for item in c.types:
        <input type="radio" name="media_type" value="${item.id}" id="radio${item.id}">
        <label for="radio${item.id}">${_(item.name.capitalize())}</label>
        % endfor
        </ul>
    </p>
    <p><textarea name="title" cols="50" rows="10"></textarea></p>
    <input type="submit" value="Process" class="button" />
</form>

</%def>
