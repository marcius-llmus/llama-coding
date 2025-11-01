from app.usage.schemas import SessionMetrics


class UsageService:
    def __init__(self):
        # This will later depend on a repository
        pass

    def get_session_metrics(self) -> SessionMetrics:
        # Placeholder logic: returns zeroed metrics.
        # In the future, this will calculate metrics for the active session.
        return SessionMetrics()


class UsagePageService:
    def __init__(self, usage_service: UsageService):
        self.usage_service = usage_service

    def get_session_metrics_page_data(self) -> dict:
        metrics = self.usage_service.get_session_metrics()
        return {"metrics": metrics}