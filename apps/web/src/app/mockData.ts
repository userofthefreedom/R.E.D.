export const projectRows = [
  {
    name: "강남 역삼동 근린시설 계획",
    address: "서울 강남구 역삼동 123-45",
    pnu: "11680-2025-123456",
    status: "진단 진행중",
    updatedAt: "2025-05-19 14:30",
    risk: "중간",
  },
  {
    name: "부산 해운대 업무시설 신축",
    address: "부산 해운대구 우동 789-10",
    pnu: "26350-2025-789012",
    status: "판정 완료",
    updatedAt: "2025-05-18 09:10",
    risk: "높음",
  },
  {
    name: "수원 권선동 공장 증축",
    address: "경기 수원시 권선구 456-7",
    pnu: "41110-2025-456789",
    status: "저장됨",
    updatedAt: "2025-05-17 17:45",
    risk: "낮음",
  },
  {
    name: "인천 송도 근린생활시설",
    address: "인천 연수구 송도동 321-8",
    pnu: "28200-2025-321987",
    status: "진단 진행중",
    updatedAt: "2025-05-16 11:22",
    risk: "중간",
  },
];

export const procedureRows = [
  {
    name: "건축심의",
    target: "대상",
    reason: "대지면적과 연면적 기준상 심의 가능성이 있습니다.",
    department: "건축과",
    risk: "중간",
  },
  {
    name: "경관심의",
    target: "비대상",
    reason: "현재 입력 기준으로 경관중점관리구역 중첩이 확인되지 않았습니다.",
    department: "경관과",
    risk: "낮음",
  },
  {
    name: "교통영향평가",
    target: "조건부",
    reason: "연면적과 용도 변경에 따라 추가 기준 확인이 필요합니다.",
    department: "교통과",
    risk: "중간",
  },
  {
    name: "재해영향평가",
    target: "대상",
    reason: "개발행위와 토지 형질변경 가능성이 있어 검토가 필요합니다.",
    department: "재난안전과",
    risk: "높음",
  },
  {
    name: "개발행위허가",
    target: "조건부",
    reason: "성토/절토 여부와 진입도로 조건을 추가 확인해야 합니다.",
    department: "도시계획과",
    risk: "중간",
  },
];

export const evidenceItems = [
  "건축법 제11조 건축허가 관련 조항",
  "국토의 계획 및 이용에 관한 법률 제56조 개발행위허가",
  "서울특별시 건축조례 주차장 설치 기준",
  "지구단위계획 시행지침 제4장 건축물 용도 제한",
];

export const missingItems = [
  "주차대수 변경 여부",
  "성토/절토 세부 규모",
  "진입도로 폭원 확인",
];

export const alternativeRows = [
  {
    name: "대안 1. 연면적 축소",
    effect: "교통영향평가와 주차기준 부담을 낮출 수 있습니다.",
    limit: "사업성 저하 가능성이 있어 내부 수지 검토가 필요합니다.",
    consultation: "건축과, 교통과 사전협의",
  },
  {
    name: "대안 2. 일부 층 용도 조정",
    effect: "지구단위계획상 용도 제한 리스크를 낮춥니다.",
    limit: "희망 업종의 운영면적이 줄어들 수 있습니다.",
    consultation: "도시계획과 사전협의",
  },
  {
    name: "대안 3. 주차계획 보완",
    effect: "용도변경 시 증가하는 주차 부담을 완화합니다.",
    limit: "기계식 주차 또는 인근 부설주차장 검토가 필요합니다.",
    consultation: "교통과, 건축과 사전협의",
  },
];

export const savedReports = [
  "종합 보고서 v1.0",
  "체크리스트 v1.0",
  "필요서류 목록 v1.0",
  "부서별 사전협의 질문 v1.0",
  "신청서/신고서 초안 v1.0",
];

export const dataSourceRows = [
  ["주소", "도로명주소 API", "실시간 조회"],
  ["필지/지도", "VWorld WMS/WFS", "조회 시점 표시"],
  ["건축물대장", "건축HUB 건축물대장정보", "API 응답 기준"],
  ["법령", "국가법령정보 공동활용", "시행일/수집일 기록"],
  ["보고서", "Rule Trace + Evidence Trace", "생성 버전 저장"],
];
