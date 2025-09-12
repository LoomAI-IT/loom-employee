import os


class Config:
    def __init__(self):
        # Service configuration
        self.service_name = os.getenv("SERVICE_NAME", "employee-service")
        self.service_version = os.getenv("SERVICE_VERSION", "1.0.0")
        self.environment = os.getenv("ENVIRONMENT", "development")
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        self.root_path = os.getenv("ROOT_PATH", "/")

        # HTTP configuration
        self.http_port = os.getenv("HTTP_PORT", "8080")
        self.prefix = os.getenv("HTTP_PREFIX", "/api/v1")

        # Database configuration
        self.db_host = os.getenv("DB_HOST", "localhost")
        self.db_port = int(os.getenv("DB_PORT", "5432"))
        self.db_name = os.getenv("DB_NAME", "employee_db")
        self.db_user = os.getenv("DB_USER", "postgres")
        self.db_pass = os.getenv("DB_PASSWORD", "postgres")

        # OpenTelemetry configuration
        self.otlp_host = os.getenv("OTLP_HOST", "localhost")
        self.otlp_port = int(os.getenv("OTLP_PORT", "4317"))

        # Alert manager configuration
        self.alert_tg_bot_token = os.getenv("ALERT_TG_BOT_TOKEN", "")
        self.alert_tg_chat_id = os.getenv("ALERT_TG_CHAT_ID", "")
        self.alert_tg_chat_thread_id = os.getenv("ALERT_TG_CHAT_THREAD_ID", "")
        self.grafana_url = os.getenv("GRAFANA_URL", "")

        # Monitoring Redis configuration
        self.monitoring_redis_host = os.getenv("MONITORING_REDIS_HOST", "localhost")
        self.monitoring_redis_port = int(os.getenv("MONITORING_REDIS_PORT", "6379"))
        self.monitoring_redis_db = int(os.getenv("MONITORING_REDIS_DB", "0"))
        self.monitoring_redis_password = os.getenv("MONITORING_REDIS_PASSWORD", "")

        # External services configuration
        self.kontur_authorization_host = os.getenv("KONTUR_AUTHORIZATION_HOST", "localhost")
        self.kontur_authorization_port = int(os.getenv("KONTUR_AUTHORIZATION_PORT", "8081"))