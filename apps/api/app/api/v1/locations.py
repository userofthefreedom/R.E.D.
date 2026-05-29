from fastapi import APIRouter

from app.clients.vworld_client import VWorldClient
from app.schemas.location import LocationCandidate, LocationResolveRequest, LocationResolveResponse

router = APIRouter()

MOCK_CANDIDATES = [
    LocationCandidate(
        pnu="41287-10123-0123456",
        standard_address="서울특별시 강남구 테헤란로 123",
        jibun_address="역삼동 123-45",
        legal_dong_code="1168051000",
        land_category="대",
        site_area=540.0,
        use_district="제2종일반주거지역",
        district_unit_plan=False,
        match_score=96,
        data_base_date="2025-05-20",
        public_data_status="정상",
        centroid_lon=127.0365,
        centroid_lat=37.5007,
        source_name="prototype mock",
    ),
    LocationCandidate(
        pnu="41287-10123-0123457",
        standard_address="서울특별시 강남구 테헤란로 123-1",
        jibun_address="역삼동 123-46",
        legal_dong_code="1168051000",
        land_category="대",
        site_area=211.3,
        use_district="제2종일반주거지역",
        district_unit_plan=False,
        match_score=81,
        data_base_date="2025-05-20",
        public_data_status="정상",
        centroid_lon=127.0372,
        centroid_lat=37.5011,
        source_name="prototype mock",
    ),
    LocationCandidate(
        pnu="41287-10123-0123458",
        standard_address="서울특별시 강남구 테헤란로 125",
        jibun_address="역삼동 123-47",
        legal_dong_code="1168051000",
        land_category="도로",
        site_area=68.2,
        use_district="도로",
        district_unit_plan=False,
        match_score=63,
        data_base_date="2025-05-20",
        public_data_status="정상",
        centroid_lon=127.0359,
        centroid_lat=37.5004,
        source_name="prototype mock",
    ),
]


def mock_geometry(lon: float, lat: float) -> dict[str, object]:
    return {
        "type": "Polygon",
        "coordinates": [[
            [lon - 0.00135, lat + 0.00075],
            [lon + 0.00100, lat + 0.00105],
            [lon + 0.00145, lat - 0.00080],
            [lon - 0.00105, lat - 0.00110],
            [lon - 0.00135, lat + 0.00075],
        ]],
    }


def build_map_click_candidates(payload: LocationResolveRequest) -> list[LocationCandidate]:
    if payload.lon is None or payload.lat is None:
        return MOCK_CANDIDATES

    vworld_candidates = VWorldClient().resolve_point(lon=payload.lon, lat=payload.lat)
    if vworld_candidates:
        return [LocationCandidate(**candidate) for candidate in vworld_candidates]

    lon_key = int(abs(payload.lon) * 10000) % 100000
    lat_key = int(abs(payload.lat) * 10000) % 100000
    base_address = f"지도 선택 위치 {payload.lat:.5f}, {payload.lon:.5f}"

    return [
        LocationCandidate(
            pnu=f"11680-{lat_key:05d}-{lon_key:07d}",
            standard_address=base_address,
            jibun_address=f"좌표기반 후보 {lat_key % 900 + 100}-{lon_key % 90 + 1}",
            legal_dong_code="1168051000",
            land_category="대",
            site_area=round(420 + (lon_key % 180) + ((lat_key % 10) * 0.7), 1),
            use_district="제2종일반주거지역",
            district_unit_plan=False,
            match_score=94,
            data_base_date="2025-05-20",
            public_data_status="지도 클릭 mock",
            centroid_lon=payload.lon,
            centroid_lat=payload.lat,
            geometry_geojson=mock_geometry(payload.lon, payload.lat),
            source_name="prototype map click resolver",
        ),
        LocationCandidate(
            pnu=f"11680-{lat_key + 1:05d}-{lon_key + 7:07d}",
            standard_address=f"{base_address} 인접 필지",
            jibun_address=f"좌표기반 후보 {lat_key % 900 + 101}-{lon_key % 90 + 2}",
            legal_dong_code="1168051000",
            land_category="대",
            site_area=round(180 + (lon_key % 120) + ((lat_key % 10) * 0.5), 1),
            use_district="제2종일반주거지역",
            district_unit_plan=False,
            match_score=78,
            data_base_date="2025-05-20",
            public_data_status="지도 클릭 mock",
            centroid_lon=payload.lon + 0.0007,
            centroid_lat=payload.lat + 0.0004,
            geometry_geojson=mock_geometry(payload.lon + 0.0007, payload.lat + 0.0004),
            source_name="prototype map click resolver",
        ),
        LocationCandidate(
            pnu=f"11680-{lat_key + 2:05d}-{lon_key + 11:07d}",
            standard_address=f"{base_address} 도로 접점",
            jibun_address=f"좌표기반 후보 {lat_key % 900 + 102}-{lon_key % 90 + 3}",
            legal_dong_code="1168051000",
            land_category="도로",
            site_area=round(60 + (lon_key % 45), 1),
            use_district="도로",
            district_unit_plan=False,
            match_score=61,
            data_base_date="2025-05-20",
            public_data_status="지도 클릭 mock",
            centroid_lon=payload.lon - 0.0006,
            centroid_lat=payload.lat - 0.0003,
            geometry_geojson=mock_geometry(payload.lon - 0.0006, payload.lat - 0.0003),
            source_name="prototype map click resolver",
        ),
    ]


@router.post("/resolve")
def resolve_location(payload: LocationResolveRequest) -> LocationResolveResponse:
    candidates = (
        build_map_click_candidates(payload)
        if payload.mode in {"coordinate", "map_click"} or payload.lon is not None or payload.lat is not None
        else MOCK_CANDIDATES
    )
    uses_vworld = any((candidate.source_name or "").startswith("VWorld") for candidate in candidates)

    return LocationResolveResponse(
        query=payload.query or (f"{payload.lat:.6f}, {payload.lon:.6f}" if payload.lon and payload.lat else ""),
        mode=payload.mode,
        status="vworld_resolved" if uses_vworld else "mock_resolved",
        provider="vworld" if uses_vworld else "prototype-location-resolver",
        candidates=candidates,
    )


@router.post("/parcel-profile")
def create_parcel_profile() -> dict[str, str]:
    return {"status": "not_implemented"}
