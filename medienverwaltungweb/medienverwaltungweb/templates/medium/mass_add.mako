<%inherit file="/layout-default.mako"/>\

<%def name="title()">${_("Add Medium")}</%def>

<%def name="content()">
<h2>${_("Add one single medium")}</h2>

<form id="signin-form" method="post" action="${h.url_for(action='mass_add_post')}">
    <p>${_("Type")}:
        <select name="media_type">
            <option value="-1">${_("Please select one")}</option>
            % for item in c.types:
            <option value="${item.id}">${_(item.name.capitalize())}</option>
            % endfor
        </select>
    </p>
    <input type="text" name="title"/>
    <input type="submit" value="Process"/>
</form>

<h2>${_("Add many media")}</h2>

<form id="signin-form" method="post" action="${h.url_for(action='mass_add_post')}">
    <p>${_("Type")}:
        <select name="media_type">
            <option value="-1">${_("Please select one")}</option>
            % for item in c.types:
            <option value="${item.id}">${_(item.name.capitalize())}</option>
            % endfor
        </select>
    </p>
    <textarea name="title" cols="50" rows="10"></textarea>
    ##<input type="text" name="openid" id="openid" class="openid-identifier" />
    <input type="submit" value="Process"/>
</form>

</%def>
