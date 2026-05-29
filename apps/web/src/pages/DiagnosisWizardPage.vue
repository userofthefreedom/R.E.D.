<script setup lang="ts">
import { computed, onMounted, ref, watch } from "vue";
import { useRoute } from "vue-router";
import {
  AlertTriangle,
  ArrowLeft,
  ArrowRight,
  CheckCircle2,
  FileText,
  Play,
  Search,
} from "@lucide/vue";
import {
  createDiagnosisRun,
  getDiagnosisResult,
  type DiagnosisResultResponse,
} from "../api/diagnosis.api";
import { resolveLocation, type LocationCandidate } from "../api/location.api";
import {
  createProject,
  createProjectAction,
  createProjectParcel,
  createProjectRegulationOverlay,
} from "../api/project.api";
import {
  actionJson,
  diagnosisMeta,
  diagnosisSummary,
  missingItems,
  pnuCandidates,
  procedureRows,
  projectRows,
  reportGenerationSteps,
  selectedParcel,
  validationAlerts,
} from "../app/mockData";
import EvidencePanel from "../components/evidence/EvidencePanel.vue";
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
import ParcelMapMock from "../components/map/ParcelMapMock.vue";
import ReportPreviewMock from "../components/report/ReportPreviewMock.vue";
import { useProjectStore } from "../stores/project.store";

const steps = [
  "위치 입력 및 PNU 변환",
  "건축 계획 입력 및 정규화",
  "판정 결과 및 근거 확인",
  "실무 산출물 생성",
];

const searchTabs = ["주소", "지번", "좌표"];
type PrototypeLocationCandidate = {
  pnu: string;
  standardAddress: string;
  jibunAddress: string;
  landCategory: string;
  siteArea: number;
  matchScore: number;
  legalDongCode: string;
  useDistrict: string;
  districtUnitPlan: boolean;
  dataBaseDate: string;
  publicDataStatus: string;
  centroidLon?: number | null;
  centroidLat?: number | null;
  geometryGeojson?: Record<string, unknown> | null;
  sourceName?: string | null;
};

type ActiveParcel = Omit<PrototypeLocationCandidate, "matchScore">;

type ActionFormState = {
  actionType: string;
  currentUse: string;
  desiredUse: string;
  siteArea: number;
  buildingArea: number | null;
  totalFloorArea: number;
  floorCountAbove: number;
  floorCountUnder: number;
  parkingBefore: number;
  parkingAfter: number;
  siteConditions: {
    earthwork: boolean;
    roadAccess: boolean;
    roadWidthCheck: boolean;
    parkingChange: boolean;
    accessRoadSecured: boolean;
    districtPlanReview: boolean;
  };
  constructionMethod: string;
  businessPurpose: string;
  memo: string;
};

const currentStep = ref(1);
const route = useRoute();
const activeSearchTab = ref("주소");
const projectStore = useProjectStore();
const isSaving = ref(false);
const locationStatus = ref("선택 완료");
const searchQuery = ref(selectedParcel.standardAddress);
const diagnosisResult = ref<DiagnosisResultResponse | null>(null);
const activeParcel = ref<ActiveParcel>({
  ...selectedParcel,
  centroidLon: 127.0365,
  centroidLat: 37.5007,
  geometryGeojson: null,
  sourceName: "기본 후보",
});
const actionForm = ref<ActionFormState>({
  actionType: "new_construction",
  currentUse: actionJson.currentUse,
  desiredUse: actionJson.desiredUse,
  siteArea: actionJson.siteArea,
  buildingArea: actionJson.buildingArea,
  totalFloorArea: actionJson.totalFloorArea,
  floorCountAbove: actionJson.floorCount.aboveGround,
  floorCountUnder: actionJson.floorCount.underground,
  parkingBefore: actionJson.parkingBefore,
  parkingAfter: actionJson.parkingAfter,
  siteConditions: { ...actionJson.siteConditions },
  constructionMethod: actionJson.constructionMethod,
  businessPurpose: actionJson.businessPurpose,
  memo: actionJson.memo,
});
const currentTitle = computed(() => steps[currentStep.value - 1]);
const normalizedAction = computed(() => ({
  actionType: actionForm.value.actionType === "new_construction" ? "신축" : actionForm.value.actionType,
  currentUse: actionForm.value.currentUse,
  desiredUse: actionForm.value.desiredUse,
  siteArea: actionForm.value.siteArea,
  buildingArea: actionForm.value.buildingArea,
  totalFloorArea: actionForm.value.totalFloorArea,
  floorCount: {
    aboveGround: actionForm.value.floorCountAbove,
    underground: actionForm.value.floorCountUnder,
  },
  parkingBefore: actionForm.value.parkingBefore,
  parkingAfter: actionForm.value.parkingAfter,
  siteConditions: actionForm.value.siteConditions,
  constructionMethod: actionForm.value.constructionMethod,
  businessPurpose: actionForm.value.businessPurpose,
  memo: actionForm.value.memo,
  parcelPnu: activeParcel.value.pnu,
}));
const actionJsonText = computed(() => JSON.stringify(normalizedAction.value, null, 2));
const displaySummary = computed(() => diagnosisResult.value?.summary ?? {
  overall: diagnosisSummary.overall,
  main_permit_type: diagnosisSummary.mainPermitType,
  risk_level: diagnosisSummary.riskLevel,
  missing_info_count: diagnosisSummary.missingInfoCount,
  required_actions: diagnosisSummary.requiredActions,
});
const displayProcedures = computed(() => diagnosisResult.value?.procedures ?? procedureRows);
const displayMissingItems = computed(() => diagnosisResult.value?.summary.required_actions ?? missingItems);
const displayRuleTraces = computed(() => diagnosisResult.value?.rule_traces ?? []);
const displayInputSnapshot = computed(() => diagnosisResult.value?.input_snapshot ?? {
  parcel_pnu: activeParcel.value.pnu,
  site_area: actionForm.value.siteArea,
  total_floor_area: actionForm.value.totalFloorArea,
  desired_use: actionForm.value.desiredUse,
  source: "service-preview",
});

function syncStepFromQuery() {
  const requestedStep = Number(route.query.step);
  if (Number.isInteger(requestedStep) && requestedStep >= 1 && requestedStep <= steps.length) {
    currentStep.value = requestedStep;
  }
}

const locationCandidates = ref<PrototypeLocationCandidate[]>(
  pnuCandidates.map((candidate) => ({
    ...candidate,
    legalDongCode: selectedParcel.legalDongCode,
    useDistrict: selectedParcel.useDistrict,
    districtUnitPlan: selectedParcel.districtUnitPlan,
    dataBaseDate: selectedParcel.dataBaseDate,
    publicDataStatus: selectedParcel.publicDataStatus,
    centroidLon: null,
    centroidLat: null,
    geometryGeojson: null,
    sourceName: "기본 후보",
  })),
);

function resetSavedDiagnosisProfile() {
  projectStore.currentParcelId = null;
  projectStore.currentRegulationOverlayId = null;
  projectStore.currentDiagnosisRunId = null;
  diagnosisResult.value = null;
}

function resetSavedActionProfile() {
  projectStore.currentActionId = null;
  projectStore.currentDiagnosisRunId = null;
  diagnosisResult.value = null;
}

function toPrototypeCandidate(candidate: LocationCandidate) {
  return {
    pnu: candidate.pnu,
    standardAddress: candidate.standard_address,
    jibunAddress: candidate.jibun_address,
    landCategory: candidate.land_category,
    siteArea: candidate.site_area,
    matchScore: candidate.match_score,
    legalDongCode: candidate.legal_dong_code,
    useDistrict: candidate.use_district,
    districtUnitPlan: candidate.district_unit_plan,
    dataBaseDate: candidate.data_base_date,
    publicDataStatus: candidate.public_data_status,
    centroidLon: candidate.centroid_lon,
    centroidLat: candidate.centroid_lat,
    geometryGeojson: candidate.geometry_geojson,
    sourceName: candidate.source_name,
  };
}

function applyLocationCandidates(candidates: LocationCandidate[]) {
  const mapped = candidates.map(toPrototypeCandidate);
  locationCandidates.value = mapped;

  const first = mapped[0];
  if (first) {
    activeParcel.value = {
      standardAddress: first.standardAddress,
      jibunAddress: first.jibunAddress,
      legalDongCode: first.legalDongCode,
      pnu: first.pnu,
      landCategory: first.landCategory,
      siteArea: first.siteArea,
      useDistrict: first.useDistrict,
      districtUnitPlan: first.districtUnitPlan,
      dataBaseDate: first.dataBaseDate,
      publicDataStatus: first.publicDataStatus,
      centroidLon: first.centroidLon,
      centroidLat: first.centroidLat,
      geometryGeojson: first.geometryGeojson,
      sourceName: first.sourceName,
    };
    actionForm.value.siteArea = first.siteArea;
    resetSavedDiagnosisProfile();
  }
}

function chooseCandidate(candidate: PrototypeLocationCandidate) {
  activeParcel.value = {
    standardAddress: candidate.standardAddress,
    jibunAddress: candidate.jibunAddress,
    legalDongCode: candidate.legalDongCode,
    pnu: candidate.pnu,
    landCategory: candidate.landCategory,
    siteArea: candidate.siteArea,
    useDistrict: candidate.useDistrict,
    districtUnitPlan: candidate.districtUnitPlan,
    dataBaseDate: candidate.dataBaseDate,
    publicDataStatus: candidate.publicDataStatus,
    centroidLon: candidate.centroidLon,
    centroidLat: candidate.centroidLat,
    geometryGeojson: candidate.geometryGeojson,
    sourceName: candidate.sourceName,
  };
  actionForm.value.siteArea = candidate.siteArea;
  resetSavedDiagnosisProfile();
}

async function ensureProjectId() {
  if (projectStore.currentProjectId) {
    return projectStore.currentProjectId;
  }

  const prototypeProject = projectRows[0];
  const project = await createProject({
    name: prototypeProject.name,
    address: prototypeProject.address,
    pnu: prototypeProject.pnu,
    description: "permit diagnosis workspace",
  });
  projectStore.currentProjectId = project.id;
  return project.id;
}

async function saveParcelProfile() {
  if (projectStore.currentParcelId) {
    return;
  }

  const projectId = await ensureProjectId();
  const parcel = await createProjectParcel(projectId, {
    pnu: activeParcel.value.pnu,
    standard_address: activeParcel.value.standardAddress,
    jibun_address: activeParcel.value.jibunAddress,
    legal_dong_code: activeParcel.value.legalDongCode,
    land_category: activeParcel.value.landCategory,
    site_area: activeParcel.value.siteArea,
    use_district: activeParcel.value.useDistrict,
    district_unit_plan: activeParcel.value.districtUnitPlan,
    geometry_geojson: activeParcel.value.geometryGeojson,
    data_base_date: activeParcel.value.dataBaseDate,
  });
  projectStore.currentParcelId = parcel.id;

  const overlay = await createProjectRegulationOverlay(projectId, {
    parcel_id: parcel.id,
    layer_code: "DISTRICT_UNIT_PLAN",
    layer_name: "지구단위계획구역",
    regulation_type: "planning",
    jurisdiction: "서울특별시 강남구",
    overlap_ratio: activeParcel.value.districtUnitPlan ? 1 : 0,
    data_base_date: activeParcel.value.dataBaseDate,
    raw_payload: { source: "default review layer", publicDataStatus: activeParcel.value.publicDataStatus },
  });
  projectStore.currentRegulationOverlayId = overlay.id;
}

async function saveActionProfile() {
  if (projectStore.currentActionId) {
    return;
  }

  const projectId = await ensureProjectId();
  const action = await createProjectAction(projectId, {
    action_type: actionForm.value.actionType,
    current_use: actionForm.value.currentUse,
    desired_use: actionForm.value.desiredUse,
    site_area: actionForm.value.siteArea,
    building_area: actionForm.value.buildingArea,
    total_floor_area: actionForm.value.totalFloorArea,
    floor_count_above: actionForm.value.floorCountAbove,
    floor_count_under: actionForm.value.floorCountUnder,
    parking_before: actionForm.value.parkingBefore,
    parking_after: actionForm.value.parkingAfter,
    site_conditions: actionForm.value.siteConditions,
    construction_method: actionForm.value.constructionMethod,
    business_purpose: actionForm.value.businessPurpose,
    memo: actionForm.value.memo,
    normalized_json: normalizedAction.value,
  });
  projectStore.currentActionId = action.id;
}

async function loadDiagnosisResult(runId: string) {
  diagnosisResult.value = await getDiagnosisResult(runId);
}

async function saveDiagnosisRun() {
  if (projectStore.currentDiagnosisRunId) {
    if (!diagnosisResult.value) {
      await loadDiagnosisResult(projectStore.currentDiagnosisRunId);
    }
    return;
  }

  const projectId = await ensureProjectId();
  const run = await createDiagnosisRun({
    project_id: projectId,
    action_id: projectStore.currentActionId,
    rule_set_version: diagnosisMeta.ruleSetVersion,
    rag_index_version: diagnosisMeta.ragIndexVersion,
    data_base_date: diagnosisMeta.dataBaseDate,
    law_base_date: diagnosisMeta.lawBaseDate,
  });
  projectStore.currentDiagnosisRunId = run.id;
  await loadDiagnosisResult(run.id);
}

async function goToStep(step: number) {
  isSaving.value = true;
  try {
    if (currentStep.value <= 1 && step > 1) {
      await saveParcelProfile();
    }
    if (currentStep.value <= 2 && step > 2) {
      await saveActionProfile();
      await saveDiagnosisRun();
    }
  } catch {
    // Prototype screens keep moving even when the local API is unavailable.
  } finally {
    isSaving.value = false;
    currentStep.value = Math.min(Math.max(step, 1), steps.length);
  }
}

const nextStep = () => goToStep(currentStep.value + 1);
const prevStep = () => (currentStep.value = Math.max(currentStep.value - 1, 1));

async function handleMapSelect(payload: { lon: number; lat: number }) {
  activeSearchTab.value = "좌표";
  isSaving.value = true;
  locationStatus.value = "공공데이터 조회 중";
  try {
    const response = await resolveLocation({
      query: `${payload.lat.toFixed(6)}, ${payload.lon.toFixed(6)}`,
      mode: "map_click",
      lon: payload.lon,
      lat: payload.lat,
    });
    applyLocationCandidates(response.candidates);
    locationStatus.value = response.provider === "vworld" ? "VWorld 조회 완료" : "기본 후보 생성";
  } catch {
    resetSavedDiagnosisProfile();
    locationStatus.value = "조회 실패 · 기존 선택 유지";
  } finally {
    isSaving.value = false;
  }
}

async function searchLocation() {
  isSaving.value = true;
  locationStatus.value = `${activeSearchTab.value} 조회 중`;
  try {
    const response = await resolveLocation({
      query: searchQuery.value,
      mode: activeSearchTab.value === "좌표" ? "coordinate" : "address",
    });
    applyLocationCandidates(response.candidates);
    locationStatus.value = response.provider === "vworld" ? "VWorld 조회 완료" : "기본 후보 생성";
  } catch {
    locationStatus.value = "조회 실패 · 기존 선택 유지";
  } finally {
    isSaving.value = false;
  }
}

onMounted(async () => {
  syncStepFromQuery();
  try {
    const response = await resolveLocation({
      query: selectedParcel.standardAddress,
      mode: "address",
    });
    applyLocationCandidates(response.candidates);
    locationStatus.value = "초기 후보 조회 완료";
  } catch {
    locationCandidates.value = pnuCandidates.map((candidate) => ({
      ...candidate,
      legalDongCode: selectedParcel.legalDongCode,
      useDistrict: selectedParcel.useDistrict,
      districtUnitPlan: selectedParcel.districtUnitPlan,
      dataBaseDate: selectedParcel.dataBaseDate,
      publicDataStatus: selectedParcel.publicDataStatus,
      centroidLon: null,
      centroidLat: null,
      geometryGeojson: null,
      sourceName: "기본 후보",
    }));
  }
});

watch(() => route.query.step, syncStepFromQuery);
watch(actionForm, resetSavedActionProfile, { deep: true });
</script>

<template>
  <AppShell>
    <PageHeader
      eyebrow="신규 사전진단 메인 플로우"
      :title="currentTitle"
      description="공공데이터, 룰엔진, RAG, LLM 산출물 생성 흐름을 하나의 사전진단 절차로 연결합니다."
    />

    <section class="diagnosis-layout">
      <aside class="panel">
        <div class="stepper">
          <button
            v-for="(step, index) in steps"
            :key="step"
            class="step-item"
            :class="{ active: currentStep === index + 1 }"
            @click="goToStep(index + 1)"
          >
            <span class="step-number">{{ index + 1 }}</span>
            <span>{{ step }}</span>
          </button>
        </div>
        <div class="notice compact-note">
          <strong>진단 기준</strong>
          <span>데이터 {{ diagnosisMeta.dataBaseDate }}</span>
          <span>법령 {{ diagnosisMeta.lawBaseDate }}</span>
          <span>{{ diagnosisMeta.ruleSetVersion }}</span>
        </div>
      </aside>

      <div class="grid">
        <section v-if="currentStep === 1" class="grid">
          <div class="result-layout">
            <div class="grid">
              <div class="panel">
                <div class="section-title">
                  <div>
                    <h2>지도에서 대상지 확인</h2>
                    <p class="subtle">주소, 지번, 좌표 또는 지도 클릭으로 필지를 확정합니다.</p>
                  </div>
                  <span class="badge">{{ isSaving ? "조회/저장 중" : locationStatus }}</span>
                </div>
                <ParcelMapMock
                  :selected-lon="activeParcel.centroidLon"
                  :selected-lat="activeParcel.centroidLat"
                  :selected-geometry="activeParcel.geometryGeojson"
                  :selected-pnu="activeParcel.pnu"
                  @select="handleMapSelect"
                />
                <div class="meta-strip">
                  <span>기준일자 {{ activeParcel.dataBaseDate }}</span>
                  <span>용도지역 {{ activeParcel.useDistrict }}</span>
                  <span>{{ activeParcel.sourceName ?? "기본 후보" }}</span>
                  <span>지구단위계획 {{ activeParcel.districtUnitPlan ? "해당" : "비해당" }}</span>
                </div>
              </div>

              <div class="panel compact-workbench">
                <div>
                  <h2>진단 준비 상태</h2>
                  <p class="subtle">확정된 PNU와 필지 프로필을 다음 단계의 Action JSON 정규화 기준으로 넘깁니다.</p>
                </div>
                <div class="readiness-grid">
                  <div><strong>Parcel Profile</strong><span>면적, 지목, 용도지역 확인 완료</span></div>
                  <div><strong>Geometry</strong><span>필지 Polygon 및 인접 도로 확인</span></div>
                  <div><strong>Public Data</strong><span>수집 기준일 {{ activeParcel.dataBaseDate }} 표시</span></div>
                  <div><strong>Next</strong><span>건축계획 입력 후 룰엔진 판단 준비</span></div>
                </div>
              </div>
            </div>

            <div class="grid">
              <div class="panel">
                <div class="section-title">
                  <h2>검색 및 후보 선택</h2>
                  <span class="badge neutral">PNU 후보 {{ locationCandidates.length }}건</span>
                </div>
                <div class="segmented-tabs">
                  <button
                    v-for="tab in searchTabs"
                    :key="tab"
                    class="segment"
                    :class="{ active: activeSearchTab === tab }"
                    @click="activeSearchTab = tab"
                  >
                    {{ tab }}
                  </button>
                </div>
                <div class="field" style="margin-top: 12px">
                  <label>{{ activeSearchTab }} 검색</label>
                  <div class="input-with-button">
                    <input v-model="searchQuery" class="input" />
                    <button class="button" type="button" @click="searchLocation"><Search />검색</button>
                  </div>
                </div>
                <ul class="candidate-list">
                  <li
                    v-for="candidate in locationCandidates"
                    :key="candidate.pnu"
                    :class="{ selected: candidate.pnu === activeParcel.pnu }"
                    @click="chooseCandidate(candidate)"
                  >
                    <div>
                      <strong>{{ candidate.pnu }}</strong>
                      <span>{{ candidate.standardAddress }}</span>
                      <span class="subtle">{{ candidate.jibunAddress }} · {{ candidate.landCategory }} · {{ candidate.siteArea }}㎡</span>
                    </div>
                    <span>
                      <span class="badge">{{ candidate.matchScore }}%</span>
                      <span class="subtle">{{ candidate.sourceName ?? "기본 후보" }}</span>
                    </span>
                  </li>
                </ul>
              </div>

              <div class="panel">
                <div class="section-title"><h2>선택된 대지 정보</h2><CheckCircle2 class="status-icon" /></div>
                <table class="table">
                  <tbody>
                    <tr><th>표준주소</th><td>{{ activeParcel.standardAddress }}</td></tr>
                    <tr><th>지번</th><td>{{ activeParcel.jibunAddress }}</td></tr>
                    <tr><th>법정동코드</th><td>{{ activeParcel.legalDongCode }}</td></tr>
                    <tr><th>PNU</th><td>{{ activeParcel.pnu }}</td></tr>
                    <tr><th>지목/면적</th><td>{{ activeParcel.landCategory }} · {{ activeParcel.siteArea }}㎡</td></tr>
                    <tr><th>용도지역</th><td>{{ activeParcel.useDistrict }}</td></tr>
                  </tbody>
                </table>
              </div>
            </div>
          </div>

        </section>

        <section v-else-if="currentStep === 2" class="result-layout">
          <div class="panel">
            <div class="section-title">
              <div>
                <h2>건축 계획 입력</h2>
                <p class="subtle">입력한 계획은 법률 판단용 문장과 Action JSON으로 변환됩니다.</p>
              </div>
              <span class="badge">필수 정보</span>
            </div>
            <div class="form-grid">
              <div class="field">
                <label>행위 유형</label>
                <select v-model="actionForm.actionType" class="select">
                  <option value="new_construction">신축</option>
                  <option value="extension">증축</option>
                  <option value="change_of_use">용도변경</option>
                </select>
              </div>
              <div class="field">
                <label>현재 용도</label>
                <select v-model="actionForm.currentUse" class="select">
                  <option>기존 건축물 없음</option>
                  <option>근린생활시설</option>
                  <option>업무시설</option>
                </select>
              </div>
              <div class="field">
                <label>희망 용도</label>
                <select v-model="actionForm.desiredUse" class="select">
                  <option>업무시설</option>
                  <option>근린생활시설</option>
                  <option>공동주택</option>
                </select>
              </div>
              <div class="field"><label>대지 면적</label><input v-model.number="actionForm.siteArea" class="input" type="number" step="0.01" /></div>
              <div class="field"><label>건축면적</label><input v-model.number="actionForm.buildingArea" class="input" type="number" step="0.01" placeholder="입력 전" /></div>
              <div class="field"><label>연면적</label><input v-model.number="actionForm.totalFloorArea" class="input" type="number" step="0.01" /></div>
              <div class="field"><label>지상 층수</label><input v-model.number="actionForm.floorCountAbove" class="input" type="number" min="0" /></div>
              <div class="field"><label>지하 층수</label><input v-model.number="actionForm.floorCountUnder" class="input" type="number" min="0" /></div>
              <div class="field"><label>주차대수 변경 전</label><input v-model.number="actionForm.parkingBefore" class="input" type="number" min="0" /></div>
              <div class="field"><label>주차대수 변경 후</label><input v-model.number="actionForm.parkingAfter" class="input" type="number" min="0" /></div>
            </div>

            <div class="condition-grid">
              <label><input v-model="actionForm.siteConditions.earthwork" type="checkbox" /> 성토/절토 있음</label>
              <label><input v-model="actionForm.siteConditions.roadAccess" type="checkbox" /> 도로 접도 확인</label>
              <label><input v-model="actionForm.siteConditions.roadWidthCheck" type="checkbox" /> 도로 폭 확인</label>
              <label><input v-model="actionForm.siteConditions.parkingChange" type="checkbox" /> 주차 변경</label>
              <label><input v-model="actionForm.siteConditions.accessRoadSecured" type="checkbox" /> 진입로 확보</label>
              <label><input v-model="actionForm.siteConditions.districtPlanReview" type="checkbox" /> 지구단위계획 검토 필요</label>
            </div>

            <div class="field" style="margin-top: 14px">
              <label>사업 목적 요약</label>
              <textarea v-model="actionForm.businessPurpose" class="textarea"></textarea>
            </div>
          </div>

          <div class="grid">
            <section class="panel">
              <h2>법률 판단용 문장</h2>
              <p>
                {{ activeParcel.standardAddress }} 소재 대지에 대하여 기존 건축물 없이 업무시설 신축을 계획하며,
                대지면적은 {{ Number(actionForm.siteArea).toFixed(2) }}㎡, 연면적은 {{ Number(actionForm.totalFloorArea).toFixed(2) }}㎡,
                지상 {{ actionForm.floorCountAbove }}층 규모입니다.
              </p>
            </section>
            <section class="panel">
              <div class="section-title"><h2>검증 알림</h2><span class="badge warning">진단 전 확인</span></div>
              <ul class="mini-list">
                <li v-for="alert in validationAlerts" :key="alert.label">
                  <span>{{ alert.label }}</span>
                  <span class="badge" :class="{ warning: alert.severity === 'warning' }">{{ alert.severity }}</span>
                </li>
              </ul>
            </section>
            <section class="panel">
              <h2>Action JSON 요약</h2>
              <pre class="code-block">{{ actionJsonText }}</pre>
            </section>
          </div>
        </section>

        <section v-else-if="currentStep === 3" class="grid">
          <div class="grid four">
            <div class="card"><span class="subtle">종합 판정</span><h2>{{ displaySummary.overall }}</h2></div>
            <div class="card"><span class="subtle">주 인허가 유형</span><h2>{{ displaySummary.main_permit_type }}</h2></div>
            <div class="card"><span class="subtle">리스크 레벨</span><h2>{{ displaySummary.risk_level }}</h2></div>
            <div class="card"><span class="subtle">누락정보</span><h2>{{ displaySummary.missing_info_count }}건</h2></div>
          </div>

          <section class="result-layout diagnosis-result-layout">
            <div class="grid">
              <div class="panel">
                <div class="section-title">
                  <div>
                    <h2>조건부 절차 목록</h2>
                    <p class="subtle">룰엔진 판단과 RAG 근거를 함께 확인하세요.</p>
                  </div>
                  <span class="badge warning">관할부서 확인 필요</span>
                </div>
                <table class="table">
                  <thead><tr><th>절차명</th><th>대상 여부</th><th>판단 사유</th><th>담당 부서</th><th>리스크</th></tr></thead>
                  <tbody>
                    <tr v-for="row in displayProcedures" :key="row.name">
                      <td>{{ row.name }}</td><td>{{ row.target }}</td><td>{{ row.reason }}</td><td>{{ row.department }}</td><td>{{ row.risk }}</td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div class="panel compact-workbench">
                <div>
                  <h2>판정 해석 메모</h2>
                  <p class="subtle">단정 대신 보완·협의 중심 표현으로 보고서에 반영됩니다.</p>
                </div>
                <div class="readiness-grid three-up">
                  <div><strong>주 절차</strong><span>{{ displaySummary.main_permit_type }} 검토 유지</span></div>
                  <div><strong>조건부 쟁점</strong><span>{{ displaySummary.required_actions.slice(0, 2).join(", ") || "추가 쟁점 낮음" }}</span></div>
                  <div><strong>보고서 문구</strong><span>{{ diagnosisResult ? "룰엔진 결과 기반" : "서비스 기준 결과 기반" }}</span></div>
                </div>
              </div>

              <section class="panel">
                <div class="section-title">
                  <div>
                    <h2>추가 검토 항목 / 누락정보</h2>
                    <p class="subtle">정보 부족, API 실패, 조례 최신성 미확인 시 단정하지 않습니다.</p>
                  </div>
                  <span class="badge warning">{{ displayMissingItems.length }}건</span>
                </div>
                <ul class="mini-list">
                  <li v-for="item in displayMissingItems" :key="item"><span>{{ item }}</span><span class="badge warning">우선순위 중간</span></li>
                </ul>
                <div class="topbar-actions" style="margin-top: 14px">
                  <RouterLink class="button" to="/projects/demo/diagnosis/alternatives"><AlertTriangle />대안 시나리오 보기</RouterLink>
                  <button class="button primary" @click="currentStep = 4"><FileText />보고서 생성으로 이동</button>
                </div>
              </section>

              <section class="panel">
                <div class="section-title">
                  <div>
                    <h2>회의용 판정 요약</h2>
                    <p class="subtle">의사결정자가 바로 확인할 수 있도록 조건, 근거, 다음 액션을 압축했습니다.</p>
                  </div>
                  <span class="badge neutral">검토본</span>
                </div>
                <div class="readiness-grid three-up">
                  <div><strong>판정</strong><span>{{ displaySummary.overall }} · {{ displaySummary.risk_level }} 리스크</span></div>
                  <div><strong>핵심 근거</strong><span>건축법, 국토계획법, 주차장 조례 기준 연결</span></div>
                  <div><strong>다음 액션</strong><span>보완자료 3건 확인 후 보고서 생성</span></div>
                </div>
              </section>
            </div>

            <div class="grid diagnosis-insight-column">
              <section class="panel">
                <div class="section-title">
                  <div>
                    <h2>Rule Trace / 입력 스냅샷</h2>
                    <p class="subtle">판정에 사용한 입력값과 최소 룰엔진 판단 근거입니다.</p>
                  </div>
                  <span class="badge">{{ diagnosisResult ? "API 결과" : "미리보기" }}</span>
                </div>
                <div class="trace-summary-grid">
                  <div class="trace-snapshot">
                    <span class="subtle">PNU</span>
                    <strong>{{ displayInputSnapshot.parcel_pnu ?? activeParcel.pnu }}</strong>
                    <span class="subtle">대지 {{ displayInputSnapshot.site_area ?? actionForm.siteArea }}㎡ · 연면적 {{ displayInputSnapshot.total_floor_area ?? actionForm.totalFloorArea }}㎡ · {{ displayInputSnapshot.desired_use ?? actionForm.desiredUse }}</span>
                  </div>
                  <div class="trace-rule-list">
                    <div v-if="!displayRuleTraces.length" class="trace-rule">
                      <strong>룰엔진 실행 전</strong>
                      <span>다음 단계 이동 시 저장된 Parcel과 Action으로 판정합니다.</span>
                    </div>
                    <div v-for="trace in displayRuleTraces" :key="trace.rule_id" class="trace-rule">
                      <strong>{{ trace.rule_name }}</strong>
                      <span>{{ trace.result }} · {{ trace.reason }}</span>
                      <small>{{ trace.input_fields.join(", ") }}</small>
                    </div>
                  </div>
                </div>
              </section>
              <EvidencePanel />
              <section class="panel">
                <div class="section-title">
                  <div>
                    <h2>사전협의 준비</h2>
                    <p class="subtle">심사위원에게 보여줄 판정 흐름과 실무 액션을 한눈에 정리했습니다.</p>
                  </div>
                  <span class="badge neutral">회의용</span>
                </div>
                <ul class="mini-list">
                  <li><span>건축과: 주 절차와 보완 기준 확인</span><span class="badge">1차</span></li>
                  <li><span>교통과: 주차대수 산정 및 도로 접도 검토</span><span class="badge warning">중점</span></li>
                  <li><span>도시계획과: 개발행위허가 조건부 여부 확인</span><span class="badge neutral">검토</span></li>
                </ul>
              </section>
            </div>
          </section>
        </section>

        <section v-else class="result-layout">
          <div class="grid">
            <section class="panel">
              <div class="section-title">
                <div>
                  <h2>실무 산출물 생성</h2>
                  <p class="subtle">체크리스트, 필요서류, 사전협의 질문, 신청서 초안, 종합 보고서를 생성합니다.</p>
                </div>
                <span class="badge">5개 선택</span>
              </div>
              <ul class="mini-list">
                <li><label><input type="checkbox" checked /> 절차별 체크리스트</label><span class="badge">Rule 기반</span></li>
                <li><label><input type="checkbox" checked /> 필요서류 목록</label><span class="badge">서류 후보</span></li>
                <li><label><input type="checkbox" checked /> 담당부서별 사전협의 질문</label><span class="badge">LLM 문서화</span></li>
                <li><label><input type="checkbox" checked /> 신청서 / 신고서 초안</label><span class="badge neutral">확인필요 포함</span></li>
                <li><label><input type="checkbox" checked /> 종합 보고서</label><span class="badge">Trace 포함</span></li>
              </ul>
            </section>
            <section class="panel">
              <div class="section-title"><h2>생성 진행 상태</h2><span class="badge warning">문서 생성 중</span></div>
              <ol class="progress-list">
                <li v-for="step in reportGenerationSteps" :key="step.name" :class="{ active: step.status === '진행 중' }">
                  <span>{{ step.name }}</span>
                  <strong>{{ step.status }}</strong>
                </li>
              </ol>
              <div class="notice" style="margin-top: 14px">
                본 서비스에서 생성되는 모든 산출물은 건축 인허가 접수 전 사전진단 참고자료입니다.
                최종 인허가 여부는 관할 행정청의 검토와 최신 법령/조례 적용에 따라 결정됩니다.
              </div>
              <div class="topbar-actions" style="margin-top: 14px">
                <button class="button"><FileText />DOCX 다운로드</button>
                <button class="button primary"><Play />PDF 다운로드</button>
              </div>
            </section>
          </div>
          <ReportPreviewMock />
        </section>

        <div class="topbar-actions" style="justify-content: space-between">
          <button class="button" :disabled="currentStep === 1" @click="prevStep"><ArrowLeft />이전</button>
          <button class="button dark" :disabled="currentStep === steps.length" @click="nextStep">다음 <ArrowRight /></button>
        </div>
      </div>
    </section>
  </AppShell>
</template>
