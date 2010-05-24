<%inherit file="/layout-default.mako"/>\

<%def name="title()">${_("Manually add Image to Media")}</%def>

<%def name="content()">
<form method="post" action="${h.url_for(controller='image', action='upload_post')}" enctype="multipart/form-data">
<p><input type="file" name="myfile"></p>
<p><input type="submit" value="${_("Upload")}" class="button" /></p>

##    <p>${_("Type")}:
##        % for item in c.types:
##        <input type="radio" name="media_type" value="${item.id}" id="radio${item.id}">
##        <label for="radio${item.id}">${_(item.name.capitalize())}</label>
##        % endfor
##        </ul>
##    </p>
##    <p><textarea name="title" cols="50" rows="10">${request.params.get('title')}</textarea></p>
</form>

</%def>
