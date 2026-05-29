from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_project_to_diagnosis_result_flow() -> None:
    project_response = client.post(
        "/api/v1/projects",
        json={
            "name": "pytest diagnosis flow",
            "address": "서울특별시 강남구 테헤란로 123",
            "pnu": "41287-10123-0123456",
        },
    )
    assert project_response.status_code == 201
    project_id = project_response.json()["id"]

    parcel_response = client.post(
        f"/api/v1/projects/{project_id}/parcels",
        json={
            "pnu": "41287-10123-0123456",
            "standard_address": "서울특별시 강남구 테헤란로 123",
            "site_area": 540,
            "geometry_geojson": {
                "type": "Polygon",
                "coordinates": [[[127, 37], [127.1, 37], [127.1, 37.1], [127, 37.1], [127, 37]]],
            },
        },
    )
    assert parcel_response.status_code == 201

    action_response = client.post(
        f"/api/v1/projects/{project_id}/actions",
        json={
            "action_type": "new_construction",
            "desired_use": "업무시설",
            "site_area": 540,
            "total_floor_area": 1200,
            "parking_after": 12,
            "site_conditions": {"roadAccess": True, "roadWidthCheck": True},
            "normalized_json": {"actionType": "신축"},
        },
    )
    assert action_response.status_code == 201

    run_response = client.post(
        "/api/v1/diagnosis/runs",
        json={"project_id": project_id, "action_id": action_response.json()["id"]},
    )
    assert run_response.status_code == 201
    assert run_response.json()["status"] == "completed"

    result_response = client.get(f"/api/v1/diagnosis/runs/{run_response.json()['id']}/result")
    assert result_response.status_code == 200
    result = result_response.json()
    assert result["summary"]["overall"] == "조건부 가능성"
    assert result["summary"]["risk_level"] == "중간"
    assert len(result["procedures"]) >= 3
    assert len(result["rule_traces"]) >= 3
