from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    ncbi_api_key: str = ""
    pubmed_max_results: int = 5
    cache_ttl_seconds: int = 3600

    mcp_port: int = 6351
    mcp_host: str = "0.0.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
