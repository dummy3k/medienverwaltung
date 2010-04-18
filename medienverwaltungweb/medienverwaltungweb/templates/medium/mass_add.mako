<%inherit file="/layout-default.mako"/>\

<%def name="title()">${_("Add Media")}</%def>

<%def name="content()">
##<h2>${_("Add one single medium")}</h2>
##<form id="signin-form" method="post" action="${h.url_for(action='mass_add_post')}">
##    <p>${_("Type")}:
##        <select name="media_type">
##            <option value="-1">${_("Please select one")}</option>
##            % for item in c.types:
##            <option value="${item.id}">${_(item.name.capitalize())}</option>
##            % endfor
##        </select>
##    </p>
##    <input type="text" name="title"/>
##    <p><input type="submit" value="${_("Process")}"/></p>
##</form>

##<h2>${_("Add many media")}</h2>

<form id="signin-form" method="post" action="${h.url_for(action='mass_add_post')}">
    <p>${_("Type")}:
##        <select name="media_type">
##            <option value="-1">${_("Please select one")}</option>
##            % for item in c.types:
##            <option value="${item.id}">${_(item.name.capitalize())}</option>
##            % endfor
##        </select>
        % for item in c.types:
        <input type="radio" name="media_type" value="${item.id}">${_(item.name.capitalize())}
        % endfor
        </ul>
    </p>
    <p><textarea name="title" cols="50" rows="10"></textarea></p>
    ##<input type="text" name="openid" id="openid" class="openid-identifier" />
    <input type="submit" value="Process"/>
</form>

</%def>
