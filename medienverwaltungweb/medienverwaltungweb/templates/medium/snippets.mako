-*- coding: utf-8 -*-
<%def name="link_to_medium(item, h)"><a href="${h.url_for(controller='medium', action='edit', id=item.id)}">${item.title}</a></%def>
