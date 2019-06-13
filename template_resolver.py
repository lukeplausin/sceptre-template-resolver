# -*- coding: utf-8 -*-

import logging

from sceptre.resolvers import Resolver
from sceptre.template import Template

class TemplateResolver(Resolver):
    """
    Resolver for templates.

    :param argument: The path to the template (does not assume a templates/ prefix)
    :type argument: str

    """

    def __init__(self, *args, **kwargs):
        super(TemplateResolver, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self._template = None
        self._resolver_started = False
        self._resolved_value = None

    def resolve(self):
        """
        Retrieves the parameter value from SSM Parameter Store.

        :returns: parameter value
        :rtype: str
        """
        if self._resolver_started:
            return self._resolved_value
        else:
            self._resolver_started = True
            if self.argument:
                # Generate template data using the sceptre template submodule
                if self._template is None:
                    self._template = Template(
                        path=self.argument,
                        sceptre_user_data=self.stack.sceptre_user_data,
                        s3_details=self.stack.s3_details,
                        connection_manager=self.stack.connection_manager
                    )
                self._resolved_value = self._template.body
                return self._resolved_value
            else:
                raise ValueError("No template path given.")
