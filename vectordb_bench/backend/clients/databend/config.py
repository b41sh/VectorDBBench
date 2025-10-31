from abc import abstractmethod
from typing import TypedDict

from pydantic import BaseModel, SecretStr

from ..api import DBCaseConfig, DBConfig, IndexType, MetricType


class DatabendConfigDict(TypedDict):
    user: str
    password: str
    host: str
    port: int
    database: str
    secure: bool


class DatabendConfig(DBConfig):
    user: str = "root"
    password: SecretStr
    host: str = "localhost"
    port: int = 8000
    db_name: str = "default"
    secure: bool = False

    def to_dict(self) -> DatabendConfigDict:
        pwd_str = self.password.get_secret_value()
        return {
            "host": self.host,
            "port": self.port,
            "database": self.db_name,
            "user": self.user,
            "password": pwd_str,
            "secure": self.secure,
        }


class DatabendIndexConfig(BaseModel, DBCaseConfig):
    metric_type: MetricType | None = None
    #vector_data_type: str | None = "Float32"  # Data type of vectors. Can be Float32 or Float64 or BFloat16
    create_index_before_load: bool = True
    create_index_after_load: bool = False
    m: int | None  # Default in databend in 32
    ef_construct: int | None  # Default in databend in 128

    def parse_metric(self) -> str:
        if not self.metric_type:
            return ""
        return self.metric_type.value

    def parse_metric_str(self) -> str:
        if self.metric_type == MetricType.L2:
            return "l2"
        if self.metric_type == MetricType.COSINE:
            return "cosine"
        return "cosine"

    @abstractmethod
    def session_param(self):
        pass

    def index_param(self) -> dict:
        return {
            "m": self.m,
            #"vector_data_type": self.vector_data_type,
            "metric_type": self.parse_metric_str(),
            "ef_construct": self.ef_construct,
        }

    def search_param(self) -> dict:
        return {}

    def session_param(self) -> dict:
        return {}
