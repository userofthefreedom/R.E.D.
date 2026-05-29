from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from sqlalchemy import Select, select
from sqlalchemy.orm import Session

from app.models.action import Action
from app.models.diagnosis_run import DiagnosisRun
from app.models.parcel import Parcel


@dataclass
class ProcedureDecision:
    name: str
    target: str
    reason: str
    department: str
    risk: str


@dataclass
class RuleTrace:
    rule_id: str
    rule_name: str
    input_fields: list[str]
    result: str
    reason: str


class RuleEngineService:
    def __init__(self, session: Session) -> None:
        self.session = session

    def evaluate_run(self, run: DiagnosisRun) -> dict[str, Any]:
        action = run.action or self.session.get(Action, run.action_id) if run.action_id else None
        parcel = self._latest_parcel(run.project_id)
        procedures, traces = self._evaluate(action, parcel)
        missing = self._missing_items(action, parcel)
        target_procedures = [item for item in procedures if item.target in {"대상", "조건부"}]

        return {
            "run_id": run.id,
            "summary": {
                "overall": "조건부 가능성" if missing or any(item.target == "조건부" for item in procedures) else "가능성 높음",
                "main_permit_type": "건축허가" if action and action.action_type == "new_construction" else "건축 인허가 검토",
                "risk_level": self._risk_level(procedures, missing),
                "missing_info_count": len(missing),
                "required_actions": missing,
            },
            "procedures": [item.__dict__ for item in procedures],
            "rule_traces": [item.__dict__ for item in traces],
            "input_snapshot": {
                "project_id": run.project_id,
                "parcel_pnu": parcel.pnu if parcel else None,
                "site_area": self._number(action.site_area if action else None),
                "total_floor_area": self._number(action.total_floor_area if action else None),
                "desired_use": action.desired_use if action else None,
                "source": "prototype-rule-engine",
            },
        }

    def _latest_parcel(self, project_id: str) -> Parcel | None:
        statement: Select[tuple[Parcel]] = (
            select(Parcel)
            .where(Parcel.project_id == project_id)
            .order_by(Parcel.created_at.desc())
            .limit(1)
        )
        return self.session.scalar(statement)

    def _evaluate(self, action: Action | None, parcel: Parcel | None) -> tuple[list[ProcedureDecision], list[RuleTrace]]:
        action_type = action.action_type if action else None
        total_floor_area = self._number(action.total_floor_area if action else None)
        site_area = self._number(action.site_area if action else None) or self._number(parcel.site_area if parcel else None)
        parking_after = action.parking_after if action else None
        site_conditions = action.site_conditions or {} if action else {}
        desired_use = action.desired_use or "" if action else ""
        district_unit_plan = bool(parcel.district_unit_plan) if parcel else False

        procedures = [
            ProcedureDecision(
                name="건축허가",
                target="대상" if action_type == "new_construction" else "조건부",
                reason="신축 행위와 연면적 조건에 따라 건축허가 검토가 필요합니다.",
                department="건축과",
                risk="보통",
            ),
            ProcedureDecision(
                name="개발행위허가",
                target="조건부" if site_conditions.get("roadAccess") or district_unit_plan else "검토",
                reason="대지 현황, 접도 조건, 지구단위계획 여부를 함께 확인해야 합니다.",
                department="도시계획과",
                risk="중간" if site_conditions.get("roadAccess") else "낮음",
            ),
            ProcedureDecision(
                name="교통영향평가",
                target="조건부" if total_floor_area >= 1000 or "업무" in desired_use else "검토",
                reason="연면적 및 용도에 따라 교통량 검토 가능성이 있습니다.",
                department="교통과",
                risk="중간" if total_floor_area >= 1000 else "낮음",
            ),
            ProcedureDecision(
                name="경관심의",
                target="비대상" if not district_unit_plan else "조건부",
                reason="현재 공간규제 중첩은 확정되지 않았으며 관할 기준 확인이 필요합니다.",
                department="경관과",
                risk="낮음",
            ),
            ProcedureDecision(
                name="주차장 조례 검토",
                target="대상" if parking_after and parking_after > 0 else "검토",
                reason="신축 또는 용도에 따른 부설주차장 설치 기준 확인이 필요합니다.",
                department="교통과",
                risk="보통" if parking_after and parking_after > 0 else "낮음",
            ),
        ]

        traces = [
            RuleTrace(
                rule_id="BUILDING_PERMIT_NEW_CONSTRUCTION",
                rule_name="신축 건축허가 기본 판단",
                input_fields=["action_type", "total_floor_area", "desired_use"],
                result=procedures[0].target,
                reason=procedures[0].reason,
            ),
            RuleTrace(
                rule_id="DEVELOPMENT_PERMISSION_SITE_CONTEXT",
                rule_name="대지 현황 및 접도 조건 검토",
                input_fields=["site_conditions.roadAccess", "parcel.district_unit_plan"],
                result=procedures[1].target,
                reason=procedures[1].reason,
            ),
            RuleTrace(
                rule_id="TRAFFIC_IMPACT_BASIC_THRESHOLD",
                rule_name="연면적 및 용도 기반 교통 검토",
                input_fields=["total_floor_area", "desired_use"],
                result=procedures[2].target,
                reason=procedures[2].reason,
            ),
        ]
        return procedures, traces

    def _missing_items(self, action: Action | None, parcel: Parcel | None) -> list[str]:
        missing: list[str] = []
        if not action:
            return ["건축계획 Action JSON 저장 필요"]
        if action.building_area is None:
            missing.append("건축면적 입력 필요")
        if action.parking_after and action.parking_after > 0:
            missing.append("주차대수 변경 후 기준 확인")
        if not parcel or not parcel.geometry_geojson:
            missing.append("필지 경계 geometry 확정 필요")
        if action.site_conditions and action.site_conditions.get("roadWidthCheck"):
            missing.append("도로 폭원 확인 자료")
        return missing

    def _risk_level(self, procedures: list[ProcedureDecision], missing: list[str]) -> str:
        if any(item.risk == "높음" for item in procedures) or len(missing) >= 4:
            return "높음"
        if any(item.risk == "중간" for item in procedures) or missing:
            return "중간"
        return "낮음"

    def _number(self, value: Any) -> float:
        if value is None:
            return 0.0
        if isinstance(value, Decimal):
            return float(value)
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0
