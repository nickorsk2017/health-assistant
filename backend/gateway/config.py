from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    client_history_agent_url: str
    doctors_agent_url: str
    gp_synthesis_agent_url: str
    labs_agent_url: str
    user_service_url: str
    device_orchestrator_agent_url: str
    complaint_manager_agent_url: str
    appointment_scheduler_agent_url: str

    cors_origins: list[str] = ["http://localhost:3000"]

    host: str = "0.0.0.0"
    port: int = 8000

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()
