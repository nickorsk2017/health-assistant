from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    openai_api_key: str
    openai_model: str = "gpt-4o"
    consilium_agent_url: str  # e.g. http://localhost:6305/mcp


    mcp_port: int = 6334
    mcp_host: str = "0.0.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
