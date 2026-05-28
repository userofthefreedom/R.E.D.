export const selectedParcel = {
  standardAddress: "서울특별시 강남구 테헤란로 123",
  jibunAddress: "역삼동 123-45",
  legalDongCode: "1168051000",
  pnu: "41287-10123-0123456",
  landCategory: "대",
  siteArea: 540.0,
  useDistrict: "제2종일반주거지역",
  districtUnitPlan: false,
  dataBaseDate: "2025-05-20",
  publicDataStatus: "정상",
};

export const pnuCandidates = [
  {
    pnu: "41287-10123-0123456",
    standardAddress: "서울특별시 강남구 테헤란로 123",
    jibunAddress: "역삼동 123-45",
    landCategory: "대",
    siteArea: 540.0,
    matchScore: 96,
  },
  {
    pnu: "41287-10123-0123457",
    standardAddress: "서울특별시 강남구 테헤란로 123-1",
    jibunAddress: "역삼동 123-46",
    landCategory: "대",
    siteArea: 211.3,
    matchScore: 81,
  },
  {
    pnu: "41287-10123-0123458",
    standardAddress: "서울특별시 강남구 테헤란로 125",
    jibunAddress: "역삼동 123-47",
    landCategory: "도로",
    siteArea: 68.2,
    matchScore: 63,
  },
];

export const layerToggles = [
  { name: "연속지적도", enabled: true },
  { name: "용도지역", enabled: true },
  { name: "지구단위계획", enabled: false },
  { name: "교육환경보호구역", enabled: true },
  { name: "도로/접도", enabled: true },
];

export const actionJson = {
  actionType: "신축",
  currentUse: "기존 건축물 없음",
  desiredUse: "업무시설",
  siteArea: 540.0,
  buildingArea: null,
  totalFloorArea: 1200.0,
  floorCount: {
    aboveGround: 5,
    underground: 0,
  },
  parkingBefore: 0,
  parkingAfter: 12,
  siteConditions: {
    earthwork: false,
    roadAccess: true,
    roadWidthCheck: true,
    parkingChange: true,
    accessRoadSecured: true,
    districtPlanReview: false,
  },
  constructionMethod: "일반 신축",
  memo: "기존 토지 매입 후 업무시설 신축 검토",
  businessPurpose: "사무실 및 근린생활시설 복합 개발",
};

export const validationAlerts = [
  { label: "주차대수 변경 후 기준 입력 필요", severity: "warning" },
  { label: "도로 폭 확인 자료 첨부 권장", severity: "warning" },
  { label: "지구단위계획 중첩 없음", severity: "success" },
];

export const diagnosisSummary = {
  overall: "조건부 가능성",
  mainPermitType: "건축허가",
  riskLevel: "중간",
  missingInfoCount: 3,
  requiredActions: ["주차대수 변경 후 기준 입력 필요", "도로 폭 확인 필요", "교통영향 검토 가능성 확인 필요"],
};

export const procedureRows = [
  {
    name: "건축허가",
    target: "대상",
    reason: "신축 및 연면적 조건에 따라 건축허가 검토가 필요합니다.",
    department: "건축과",
    risk: "보통",
  },
  {
    name: "개발행위허가",
    target: "조건부",
    reason: "대지 현황 및 도로 접도 조건 추가 확인이 필요합니다.",
    department: "도시계획과",
    risk: "중간",
  },
  {
    name: "교통영향평가",
    target: "조건부",
    reason: "연면적 및 용도에 따라 교통량 검토가 필요합니다.",
    department: "교통과",
    risk: "중간",
  },
  {
    name: "경관심의",
    target: "비대상",
    reason: "현재 공간규제 중첩이 확인되지 않았습니다.",
    department: "경관과",
    risk: "낮음",
  },
  {
    name: "주차장 조례 검토",
    target: "대상",
    reason: "신축 시 주차대수 기준 확인이 필요합니다.",
    department: "교통과",
    risk: "보통",
  },
];

export const evidenceItems = [
  {
    title: "건축법 제11조",
    detail: "건축허가 대상 판단의 기본 근거",
    source: "국가법령정보 공동활용",
    date: "2025-05-20",
  },
  {
    title: "국토의 계획 및 이용에 관한 법률 제56조",
    detail: "토지의 형질변경 및 개발행위허가 검토 근거",
    source: "국가법령정보 공동활용",
    date: "2025-05-20",
  },
  {
    title: "서울특별시 주차장 설치 및 관리 조례",
    detail: "업무시설 신축에 따른 부설주차장 설치 기준",
    source: "자치법규정보시스템",
    date: "2025-05-20",
  },
  {
    title: "강남구 도시계획조례",
    detail: "용도지역 내 건축행위 제한 및 심의 가능성 검토",
    source: "자치법규정보시스템",
    date: "2025-05-20",
  },
];

export const evidenceTraces = [
  {
    procedure: "개발행위허가",
    source: "국토의 계획 및 이용에 관한 법률 제56조",
    chunkId: "LAW-NLPA-56-001",
    reason: "토지의 형질변경 및 개발행위 허가 대상 여부 판단 근거",
    confidence: 0.87,
  },
  {
    procedure: "건축허가",
    source: "건축법 제11조",
    chunkId: "LAW-BA-11-002",
    reason: "신축 계획의 주 인허가 유형 판단 근거",
    confidence: 0.91,
  },
  {
    procedure: "주차장 조례 검토",
    source: "서울특별시 주차장 설치 및 관리 조례",
    chunkId: "ORD-SEOUL-PARKING-014",
    reason: "업무시설 신축 시 부설주차장 기준 확인",
    confidence: 0.82,
  },
];

export const ruleTraces = [
  {
    ruleId: "MAIN-NEW-001",
    ruleName: "신축 주 인허가 유형 분기",
    inputFields: ["action.actionType", "parcel.siteArea", "action.totalFloorArea"],
    result: "건축허가 검토",
    reason: "기존 건축물 없음 및 신축 계획으로 주절차 후보 생성",
  },
  {
    ruleId: "DEV-ACT-001",
    ruleName: "개발행위허가 검토 룰",
    inputFields: ["action.actionType", "parcel.landCategory", "siteConditions.roadAccess"],
    result: "조건부 검토",
    reason: "신축 계획과 대지 조건에 따라 개발행위허가 검토 필요",
  },
  {
    ruleId: "PARKING-LOCAL-002",
    ruleName: "부설주차장 조례 검토",
    inputFields: ["action.desiredUse", "action.parkingAfter", "action.totalFloorArea"],
    result: "대상",
    reason: "업무시설 신축 및 주차대수 변경으로 조례 기준 확인 필요",
  },
];

export const diagnosisMeta = {
  dataBaseDate: "2025-05-20",
  lawBaseDate: "2025-05-20",
  ruleSetVersion: "rule-set-v0.1.0",
  ragIndexVersion: "legal-index-v0.1.0",
};

export const missingItems = ["주차대수 변경 후 기준", "성토/절토 세부 규모", "진입도로 폭원 확인"];

export const similarCases = [
  {
    title: "강남구 근린생활시설 신축 검토 사례",
    similarity: 85,
    region: "서울 강남구",
    useDistrict: "제2종일반주거지역",
    landCategory: "대",
    result: "조건부 승인",
    referencePoint: "주차대수 보완 및 도로 접도 확인 후 진행",
  },
  {
    title: "송파구 업무시설 용도변경 사례",
    similarity: 78,
    region: "서울 송파구",
    useDistrict: "일반상업지역",
    landCategory: "대",
    result: "사전협의 후 보완",
    referencePoint: "교통량 검토와 부서 협의 선행",
  },
];

export const alternativeRows = [
  {
    name: "연면적 축소",
    effect: "교통영향 및 주차 부담을 완화합니다.",
    limit: "사업성 저하 가능성이 있어 내부 수지 검토가 필요합니다.",
    consultation: "건축과, 교통과",
    score: 82,
  },
  {
    name: "일부 용도 조정",
    effect: "허용용도 충돌 가능성을 낮춥니다.",
    limit: "수익 구조와 임대 전략 변경이 필요합니다.",
    consultation: "도시계획과",
    score: 76,
  },
  {
    name: "주차계획 보완",
    effect: "주차장 조례 리스크를 완화합니다.",
    limit: "추가 비용 및 설계 변경이 발생할 수 있습니다.",
    consultation: "교통과, 건축과",
    score: 88,
  },
];

export const reportGenerationSteps = [
  { name: "보고서 컨텍스트 구성 중", status: "완료" },
  { name: "근거 정리 중", status: "완료" },
  { name: "문서 생성 중", status: "진행 중" },
  { name: "다운로드 준비 완료", status: "대기" },
];

export const savedReports = [
  "종합 보고서 v1.0",
  "절차별 체크리스트 v1.0",
  "필요서류 목록 v1.0",
  "부서별 사전협의 질문 v1.0",
  "신청서/신고서 초안 v1.0",
];

export const projectRows = [
  {
    id: "p-001",
    name: "강남 역삼동 근린시설 계획",
    address: "서울 강남구 역삼동 123-45",
    pnu: "11680-2025-123456",
    status: "진단 진행중",
    updatedAt: "2025-05-19 14:30",
    risk: "중간",
    action: "이어하기",
  },
  {
    id: "p-002",
    name: "부산 해운대 업무시설 신축",
    address: "부산 해운대구 우동 789-10",
    pnu: "26350-2025-789012",
    status: "판정 완료",
    updatedAt: "2025-05-18 09:10",
    risk: "높음",
    action: "결과 보기",
  },
  {
    id: "p-003",
    name: "수원 권선동 공동주택",
    address: "경기 수원시 권선구 권선동 456-7",
    pnu: "41110-2025-456789",
    status: "보고서 생성됨",
    updatedAt: "2025-05-17 17:45",
    risk: "낮음",
    action: "다운로드",
  },
  {
    id: "p-004",
    name: "인천 송도 근린생활시설",
    address: "인천 연수구 송도동 321-8",
    pnu: "28200-2025-321987",
    status: "추가정보 필요",
    updatedAt: "2025-05-16 11:22",
    risk: "중간",
    action: "보완하기",
  },
];

export const recentNotifications = [
  "강남 역삼동 계획의 주차 기준 확인이 필요합니다.",
  "법령 인덱스 legal-index-v0.1.0 기준으로 근거가 갱신되었습니다.",
  "부산 해운대 프로젝트의 보고서 v1.0이 생성되었습니다.",
];

export const dataSourceRows = [
  ["주소", "도로명주소 API", "실시간 조회"],
  ["필지/지도", "VWorld WMS/WFS", "조회 시점 표시"],
  ["건축물대장", "건축HUB 건축물대장정보", "API 응답 기준"],
  ["법령", "국가법령정보 공동활용", "시행일/수집일 기록"],
  ["보고서", "Rule Trace + Evidence Trace", "생성 버전 저장"],
];
