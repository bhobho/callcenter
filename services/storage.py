import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class CallDataStorage:
    """Store and retrieve call data locally"""

    def __init__(self, storage_dir: str = "./data"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(exist_ok=True)
        self.calls_dir = self.storage_dir / "calls"
        self.calls_dir.mkdir(exist_ok=True)
        self.metadata_file = self.storage_dir / "metadata.json"

        logger.info(f"Storage initialized at {self.storage_dir}")

    def save_call(self, call_data: Dict) -> bool:
        """Save call data to file"""
        try:
            call_sid = call_data.get("call_sid")
            if not call_sid:
                logger.error("Cannot save call without call_sid")
                return False

            # Create call-specific file
            call_file = self.calls_dir / f"{call_sid}.json"

            # Add timestamp if not present
            if "saved_at" not in call_data:
                call_data["saved_at"] = datetime.utcnow().isoformat()

            with open(call_file, "w") as f:
                json.dump(call_data, f, indent=2)

            logger.info(f"Call data saved: {call_sid}")

            # Update metadata
            self._update_metadata(call_data)

            return True

        except Exception as e:
            logger.error(f"Error saving call data: {e}")
            return False

    def get_call(self, call_sid: str) -> Optional[Dict]:
        """Retrieve call data by ID"""
        try:
            call_file = self.calls_dir / f"{call_sid}.json"

            if not call_file.exists():
                logger.warning(f"Call not found: {call_sid}")
                return None

            with open(call_file, "r") as f:
                return json.load(f)

        except Exception as e:
            logger.error(f"Error retrieving call data: {e}")
            return None

    def get_all_calls(self, limit: int = 100) -> List[Dict]:
        """Get all stored calls"""
        try:
            calls = []
            call_files = sorted(
                self.calls_dir.glob("*.json"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )[:limit]

            for call_file in call_files:
                with open(call_file, "r") as f:
                    calls.append(json.load(f))

            return calls

        except Exception as e:
            logger.error(f"Error retrieving calls: {e}")
            return []

    def get_call_statistics(self) -> Dict:
        """Get statistics about stored calls"""
        try:
            calls = self.get_all_calls(limit=None)

            if not calls:
                return {
                    "total_calls": 0,
                    "average_duration": 0,
                    "total_duration": 0,
                }

            total_calls = len(calls)
            total_duration = sum(
                call.get("duration_seconds", 0) for call in calls
            )
            average_duration = total_duration / total_calls if total_calls > 0 else 0

            return {
                "total_calls": total_calls,
                "average_duration": average_duration,
                "total_duration": total_duration,
            }

        except Exception as e:
            logger.error(f"Error calculating statistics: {e}")
            return {}

    def _update_metadata(self, call_data: Dict):
        """Update metadata file with call information"""
        try:
            metadata = {}

            if self.metadata_file.exists():
                with open(self.metadata_file, "r") as f:
                    metadata = json.load(f)

            # Update call count
            if "total_calls" not in metadata:
                metadata["total_calls"] = 0
            metadata["total_calls"] += 1

            # Update last call timestamp
            metadata["last_call_at"] = datetime.utcnow().isoformat()

            # Track call sources
            if "calls_by_source" not in metadata:
                metadata["calls_by_source"] = {}

            from_number = call_data.get("from", "unknown")
            if from_number not in metadata["calls_by_source"]:
                metadata["calls_by_source"][from_number] = 0
            metadata["calls_by_source"][from_number] += 1

            with open(self.metadata_file, "w") as f:
                json.dump(metadata, f, indent=2)

        except Exception as e:
            logger.error(f"Error updating metadata: {e}")

    def delete_old_calls(self, days: int = 30) -> int:
        """Delete calls older than specified days"""
        try:
            from datetime import timedelta

            cutoff_time = datetime.utcnow() - timedelta(days=days)
            deleted_count = 0

            for call_file in self.calls_dir.glob("*.json"):
                file_mtime = datetime.fromtimestamp(call_file.stat().st_mtime)

                if file_mtime < cutoff_time:
                    call_file.unlink()
                    deleted_count += 1

            logger.info(f"Deleted {deleted_count} old call files")
            return deleted_count

        except Exception as e:
            logger.error(f"Error deleting old calls: {e}")
            return 0

    def export_calls_csv(self, output_file: str = "calls_export.csv") -> bool:
        """Export calls to CSV format"""
        try:
            import csv

            calls = self.get_all_calls(limit=None)

            if not calls:
                logger.warning("No calls to export")
                return False

            # Get all possible keys
            all_keys = set()
            for call in calls:
                all_keys.update(call.keys())

            with open(output_file, "w", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=sorted(all_keys))
                writer.writeheader()

                for call in calls:
                    # Flatten nested structures
                    flattened = {}
                    for key, value in call.items():
                        if isinstance(value, (list, dict)):
                            flattened[key] = json.dumps(value)
                        else:
                            flattened[key] = value

                    writer.writerow(flattened)

            logger.info(f"Exported {len(calls)} calls to {output_file}")
            return True

        except Exception as e:
            logger.error(f"Error exporting calls: {e}")
            return False
