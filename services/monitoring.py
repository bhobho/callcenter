import logging
from datetime import datetime
from typing import Dict, List
from collections import defaultdict

logger = logging.getLogger(__name__)


class CallMetrics:
    """Track metrics for a single call"""

    def __init__(self, call_sid: str):
        self.call_sid = call_sid
        self.start_time = datetime.utcnow()
        self.end_time = None
        self.message_count = 0
        self.error_count = 0
        self.low_confidence_count = 0
        self.total_duration = 0

    def add_message(self):
        self.message_count += 1

    def add_error(self):
        self.error_count += 1

    def add_low_confidence(self):
        self.low_confidence_count += 1

    def end(self):
        self.end_time = datetime.utcnow()
        self.total_duration = (self.end_time - self.start_time).total_seconds()

    def to_dict(self) -> Dict:
        return {
            "call_sid": self.call_sid,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "duration_seconds": self.total_duration,
            "message_count": self.message_count,
            "error_count": self.error_count,
            "low_confidence_count": self.low_confidence_count,
        }


class MonitoringService:
    """Monitor application health and call metrics"""

    def __init__(self):
        self.call_metrics: Dict[str, CallMetrics] = {}
        self.system_errors: List[Dict] = []
        self.api_usage = defaultdict(int)

    def start_call_metrics(self, call_sid: str) -> CallMetrics:
        """Start tracking metrics for a call"""
        metrics = CallMetrics(call_sid)
        self.call_metrics[call_sid] = metrics
        logger.info(f"Started metrics tracking for {call_sid}")
        return metrics

    def record_message(self, call_sid: str):
        """Record a message in a call"""
        if call_sid in self.call_metrics:
            self.call_metrics[call_sid].add_message()

    def record_error(self, call_sid: str, error: str):
        """Record an error for a call"""
        if call_sid in self.call_metrics:
            self.call_metrics[call_sid].add_error()

        self.system_errors.append({
            "call_sid": call_sid,
            "error": error,
            "timestamp": datetime.utcnow().isoformat()
        })
        logger.error(f"Error recorded for {call_sid}: {error}")

    def record_low_confidence(self, call_sid: str):
        """Record a low confidence transcription"""
        if call_sid in self.call_metrics:
            self.call_metrics[call_sid].add_low_confidence()

    def end_call_metrics(self, call_sid: str):
        """End tracking for a call"""
        if call_sid in self.call_metrics:
            self.call_metrics[call_sid].end()
            logger.info(f"Metrics ended for {call_sid}: {self.call_metrics[call_sid].to_dict()}")

    def record_api_usage(self, service: str, tokens: int = 1):
        """Record API usage"""
        self.api_usage[service] += tokens

    def get_call_metrics(self, call_sid: str) -> Dict:
        """Get metrics for a specific call"""
        if call_sid in self.call_metrics:
            return self.call_metrics[call_sid].to_dict()
        return {}

    def get_all_metrics(self) -> Dict:
        """Get all metrics"""
        return {
            "calls": {sid: metrics.to_dict() for sid, metrics in self.call_metrics.items()},
            "total_calls": len(self.call_metrics),
            "errors": len(self.system_errors),
            "api_usage": dict(self.api_usage),
        }

    def get_health_status(self) -> Dict:
        """Get overall health status"""
        total_calls = len(self.call_metrics)
        total_errors = len(self.system_errors)
        error_rate = (total_errors / total_calls * 100) if total_calls > 0 else 0

        return {
            "status": "healthy" if error_rate < 10 else "degraded" if error_rate < 25 else "critical",
            "total_calls": total_calls,
            "total_errors": total_errors,
            "error_rate_percent": error_rate,
            "api_usage": dict(self.api_usage),
        }

    def cleanup_old_metrics(self, keep_count: int = 1000):
        """Remove old metrics to free memory"""
        if len(self.call_metrics) > keep_count:
            # Keep only the most recent calls
            sorted_calls = sorted(
                self.call_metrics.items(),
                key=lambda x: x[1].start_time,
                reverse=True
            )
            self.call_metrics = dict(sorted_calls[:keep_count])
            logger.info(f"Cleaned up metrics, keeping {keep_count} most recent")
