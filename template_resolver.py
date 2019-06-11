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

    def resolve(self):
        """
        Retrieves the parameter value from SSM Parameter Store.

        :returns: parameter value
        :rtype: str
        """
        if self.argument:
            file_path = self.argument
            stack = self.stack.sceptre_user_data
        
            # Generate template data using the sceptre template submodule
            if self._template is None:
                self._template = Template(
                    path=file_path,
                    sceptre_user_data=self.stack.sceptre_user_data,
                    s3_details=self.stack.s3_details,
                    connection_manager=self.stack.connection_manager
                )
            return self._template.body
        else:
            raise ValueError("No template path given.")

        # decoded_value = None
        # if self.argument:
        #     param = self.argument
        #     connection_manager = self.stack.connection_manager
        #     try:
        #         response = connection_manager.call(
        #             service="ssm",
        #             command="get_parameter",
        #             kwargs={"Name": param,
        #                     "WithDecryption": True},
        #             profile=self.stack.profile,
        #             region=self.stack.region,
        #             stack_name=self.stack.name
        #         )
        #     except ClientError as e:
        #         if "ParameterNotFound" in e.response["Error"]["Code"]:
        #             self.logger.error("%s - ParameterNotFound: %s",
        #                               self.stack.name, param)
        #         raise e
        #     decoded_value = response['Parameter']['Value']
        # return decoded_value
