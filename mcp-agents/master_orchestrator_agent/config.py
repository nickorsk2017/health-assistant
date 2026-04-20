from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    client_history_agent_url: str = "http://localhost:6332/mcp"
    labs_agent_url: str = "http://localhost:6444/mcp"
    doctors_agent_url: str = "http://localhost:6333/mcp"
    gp_synthesis_agent_url: str = "http://localhost:6334/mcp"
    pubmed_validator_agent_url: str = "http://localhost:6351/mcp"
    device_orchestrator_agent_url: str = "http://localhost:6340/mcp"
    complaint_manager_agent_url: str = "http://localhost:6341/mcp"

    mcp_port: int = 6350
    mcp_host: str = "0.0.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
