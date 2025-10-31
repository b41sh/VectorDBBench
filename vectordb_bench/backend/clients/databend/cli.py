from typing import Annotated, TypedDict, Unpack

import click
from pydantic import SecretStr

from ....cli.cli import (
    CommonTypedDict,
    HNSWFlavor2,
    cli,
    click_parameter_decorators_from_typed_dict,
    run,
)
from .. import DB
from .config import DatabendHNSWConfig


class DatabendTypedDict(TypedDict):
    password: Annotated[str, click.option("--password", type=str, help="DB password")]
    host: Annotated[str, click.option("--host", type=str, help="DB host", required=True)]
    port: Annotated[int, click.option("--port", type=int, default=8123, help="DB Port")]
    user: Annotated[int, click.option("--user", type=str, default="databend", help="DB user")]
    ssl: Annotated[
        bool,
        click.option(
            "--ssl/--no-ssl",
            is_flag=True,
            show_default=True,
            default=True,
            help="Enable or disable SSL for Databend",
        ),
    ]
    ssl_ca_certs: Annotated[
        str,
        click.option(
            "--ssl-ca-certs",
            show_default=True,
            help="Path to certificate authority file to use for SSL",
        ),
    ]


class DatabendHNSWTypedDict(CommonTypedDict, DatabendTypedDict, HNSWFlavor2): ...


@cli.command()
@click_parameter_decorators_from_typed_dict(DatabendHNSWTypedDict)
def Databend(**parameters: Unpack[DatabendHNSWTypedDict]):
    from .config import DatabendConfig

    run(
        db=DB.Databend,
        db_config=DatabendConfig(
            db_label=parameters["db_label"],
            user=parameters["user"],
            password=SecretStr(parameters["password"]) if parameters["password"] else None,
            host=parameters["host"],
            port=parameters["port"],
            ssl=parameters["ssl"],
            ssl_ca_certs=parameters["ssl_ca_certs"],
        ),
        db_case_config=DatabendHNSWConfig(
            M=parameters["m"],
            efConstruction=parameters["ef_construction"],
            ef=parameters["ef_runtime"],
        ),
        **parameters,
    )
