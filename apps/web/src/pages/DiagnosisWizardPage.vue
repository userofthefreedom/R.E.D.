<script setup lang="ts">
import { computed, ref } from "vue";
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
  actionJson,
  diagnosisMeta,
  diagnosisSummary,
  missingItems,
  pnuCandidates,
  procedureRows,
  reportGenerationSteps,
  selectedParcel,
  validationAlerts,
} from "../app/mockData";
import EvidencePanel from "../components/evidence/EvidencePanel.vue";
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
import ParcelMapMock from "../components/map/ParcelMapMock.vue";
import ReportPreviewMock from "../components/report/ReportPreviewMock.vue";

const steps = [
  "위치 입력 및 PNU 변환",
  "건축 계획 입력 및 정규화",
  "판정 결과 및 근거 확인",
  "실무 산출물 생성",
];

const searchTabs = ["주소", "지번", "좌표"];
const currentStep = ref(1);
const activeSearchTab = ref("주소");
const currentTitle = computed(() => steps[currentStep.value - 1]);
const actionJsonText = computed(() => JSON.stringify(actionJson, null, 2));
const nextStep = () => (currentStep.value = Math.min(currentStep.value + 1, steps.length));
const prevStep = () => (currentStep.value = Math.max(currentStep.value - 1, 1));
</script>

<template>
  <AppShell>
    <PageHeader
      eyebrow="신규 사전진단 메인 플로우"
      :title="currentTitle"
      description="공공데이터, 룰엔진, RAG, LLM 산출물 생성 흐름을 mock data로 연결한 프로토타입입니다."
    />

    <section class="diagnosis-layout">
      <aside class="panel">
        <div class="stepper">
          <button
            v-for="(step, index) in steps"
            :key="step"
            class="step-item"
            :class="{ active: currentStep === index + 1 }"
            @click="currentStep = index + 1"
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
        <section v-if="currentStep === 1" class="result-layout">
          <div class="panel">
            <div class="section-title">
              <div>
                <h2>지도에서 대상지 확인</h2>
                <p class="subtle">주소, 지번, 좌표 또는 지도 클릭으로 필지를 확정합니다.</p>
              </div>
              <span class="badge">공공데이터 조회 상태: 정상</span>
            </div>
            <ParcelMapMock />
            <div class="meta-strip">
              <span>기준일자 {{ selectedParcel.dataBaseDate }}</span>
              <span>용도지역 {{ selectedParcel.useDistrict }}</span>
              <span>지구단위계획 {{ selectedParcel.districtUnitPlan ? "해당" : "비해당" }}</span>
            </div>
          </div>

          <div class="grid">
            <div class="panel">
              <div class="section-title">
                <h2>검색 및 후보 선택</h2>
                <span class="badge neutral">PNU 후보 {{ pnuCandidates.length }}건</span>
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
                  <input class="input" value="서울특별시 강남구 테헤란로 123" />
                  <button class="button"><Search />검색</button>
                </div>
              </div>
              <ul class="candidate-list">
                <li v-for="candidate in pnuCandidates" :key="candidate.pnu" :class="{ selected: candidate.pnu === selectedParcel.pnu }">
                  <div>
                    <strong>{{ candidate.pnu }}</strong>
                    <span>{{ candidate.standardAddress }}</span>
                    <span class="subtle">{{ candidate.jibunAddress }} · {{ candidate.landCategory }} · {{ candidate.siteArea }}㎡</span>
                  </div>
                  <span class="badge">{{ candidate.matchScore }}%</span>
                </li>
              </ul>
            </div>

            <div class="panel">
              <div class="section-title"><h2>선택된 대지 정보</h2><CheckCircle2 class="status-icon" /></div>
              <table class="table">
                <tbody>
                  <tr><th>표준주소</th><td>{{ selectedParcel.standardAddress }}</td></tr>
                  <tr><th>지번</th><td>{{ selectedParcel.jibunAddress }}</td></tr>
                  <tr><th>법정동코드</th><td>{{ selectedParcel.legalDongCode }}</td></tr>
                  <tr><th>PNU</th><td>{{ selectedParcel.pnu }}</td></tr>
                  <tr><th>지목/면적</th><td>{{ selectedParcel.landCategory }} · {{ selectedParcel.siteArea }}㎡</td></tr>
                  <tr><th>용도지역</th><td>{{ selectedParcel.useDistrict }}</td></tr>
                </tbody>
              </table>
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
              <div class="field"><label>행위 유형</label><select class="select"><option>신축</option></select></div>
              <div class="field"><label>현재 용도</label><select class="select"><option>기존 건축물 없음</option></select></div>
              <div class="field"><label>희망 용도</label><select class="select"><option>업무시설</option></select></div>
              <div class="field"><label>기존 건축물 여부</label><select class="select"><option>없음</option></select></div>
              <div class="field"><label>대지 면적</label><input class="input" value="540.00 ㎡" /></div>
              <div class="field"><label>건축면적</label><input class="input" placeholder="입력 전" /></div>
              <div class="field"><label>연면적</label><input class="input" value="1,200.00 ㎡" /></div>
              <div class="field"><label>층수</label><input class="input" value="지상 5층 / 지하 0층" /></div>
              <div class="field"><label>주차대수 변경 전</label><input class="input" value="0대" /></div>
              <div class="field"><label>주차대수 변경 후</label><input class="input" value="12대" /></div>
            </div>

            <div class="condition-grid">
              <label><input type="checkbox" /> 성토/절토 있음</label>
              <label><input type="checkbox" checked /> 도로 접도 확인</label>
              <label><input type="checkbox" checked /> 도로 폭 확인</label>
              <label><input type="checkbox" checked /> 주차 변경</label>
              <label><input type="checkbox" checked /> 진입로 확보</label>
              <label><input type="checkbox" /> 지구단위계획 검토 필요</label>
            </div>

            <div class="field" style="margin-top: 14px">
              <label>사업 목적 요약</label>
              <textarea class="textarea">사무실 및 근린생활시설 복합 개발</textarea>
            </div>
          </div>

          <div class="grid">
            <section class="panel">
              <h2>법률 판단용 문장</h2>
              <p>
                {{ selectedParcel.standardAddress }} 소재 대지에 대하여 기존 건축물 없이 업무시설 신축을 계획하며,
                대지면적은 540.00㎡, 연면적은 1,200.00㎡, 지상 5층 규모입니다.
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
            <div class="card"><span class="subtle">종합 판정</span><h2>{{ diagnosisSummary.overall }}</h2></div>
            <div class="card"><span class="subtle">주 인허가 유형</span><h2>{{ diagnosisSummary.mainPermitType }}</h2></div>
            <div class="card"><span class="subtle">리스크 레벨</span><h2>{{ diagnosisSummary.riskLevel }}</h2></div>
            <div class="card"><span class="subtle">누락정보</span><h2>{{ diagnosisSummary.missingInfoCount }}건</h2></div>
          </div>

          <section class="result-layout">
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
                  <tr v-for="row in procedureRows" :key="row.name">
                    <td>{{ row.name }}</td><td>{{ row.target }}</td><td>{{ row.reason }}</td><td>{{ row.department }}</td><td>{{ row.risk }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <EvidencePanel />
          </section>

          <section class="panel">
            <div class="section-title">
              <div>
                <h2>추가 검토 항목 / 누락정보</h2>
                <p class="subtle">정보 부족, API 실패, 조례 최신성 미확인 시 단정하지 않습니다.</p>
              </div>
              <span class="badge warning">{{ missingItems.length }}건</span>
            </div>
            <ul class="mini-list">
              <li v-for="item in missingItems" :key="item"><span>{{ item }}</span><span class="badge warning">우선순위 중간</span></li>
            </ul>
            <div class="topbar-actions" style="margin-top: 14px">
              <RouterLink class="button" to="/projects/demo/diagnosis/alternatives"><AlertTriangle />대안 시나리오 보기</RouterLink>
              <button class="button primary" @click="currentStep = 4"><FileText />보고서 생성으로 이동</button>
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
