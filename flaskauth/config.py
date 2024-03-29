import json
import os
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError, NoCredentialsError
from flask import Flask
from jsonlogger import LOG

CONFIG = {}


def load_ssm_parameters(app):
    ssm_parameters_retrieved = True
    try:

        ssm_prefix = os.environ.get("SSM_PREFIX")
        if ssm_prefix:
            ssm_parameter_map = {
                "/oidc/endpoint": "oidc_endpoint",
                "/oidc/client_id": "oidc_client_id",
                "/oidc/client_secret": "oidc_client_secret",  # pragma: allowlist secret
                "/flask/secret_key": "secret_key",  # pragma: allowlist secret
            }

            ssm_client = boto3.client("ssm")

            ssm_parameters = ssm_client.get_parameters_by_path(
                Path=ssm_prefix, Recursive=True, WithDecryption=True
            )
            LOG.debug(str(ssm_parameters))
            for param in ssm_parameters["Parameters"]:
                for param_name, config_var_name in ssm_parameter_map.items():
                    if param["Name"].endswith(param_name):

                        # The flask secret_key is attached directly to app
                        # instead of set in app.config
                        if config_var_name == "secret_key":
                            LOG.debug("Set app property: %s from ssm", config_var_name)
                            app.secret_key = param["Value"]
                            app.config["SECRET_KEY"] = param["Value"]

                        CONFIG[config_var_name] = param["Value"]
                        LOG.debug("Set config var: %s from ssm", config_var_name)
        else:
            LOG.debug("No SSM prefix - try loading creds from env")
            try:
                secret_key = str(uuid4()).encode()
                CONFIG["oidc_client_id"] = os.environ["OIDC_CLIENT_ID"]
                CONFIG["oidc_client_secret"] = os.environ["OIDC_CLIENT_SECRET"]
                CONFIG["oidc_endpoint"] = os.environ["OIDC_ENDPOINT"]
                CONFIG["oidc_scopes"] = os.environ.get("OIDC_SCOPES", "openid profile email")
                CONFIG["secret_key"] = os.environ.get("FLASK_SECRET", secret_key)

                app.secret_key = os.environ.get("FLASK_SECRET", secret_key)
                LOG.debug(app.secret_key)
            except (KeyError) as error:
                LOG.debug("No credentials")
        LOG.debug("Config module settings")
        LOG.debug(CONFIG.keys())
        app.config.update(CONFIG)

    except (ClientError, KeyError, ValueError) as error:
        LOG.error(error)
        ssm_parameters_retrieved = False
    except NoCredentialsError as error:
        LOG.debug(error)
        ssm_parameters_retrieved = False

    return ssm_parameters_retrieved
