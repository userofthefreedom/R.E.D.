<script setup lang="ts">
import { computed, ref } from "vue";
import { AlertTriangle, ArrowLeft, ArrowRight, FileText, Play } from "@lucide/vue";
import { missingItems, procedureRows } from "../app/mockData";
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

const currentStep = ref(1);
const currentTitle = computed(() => steps[currentStep.value - 1]);
const nextStep = () => (currentStep.value = Math.min(currentStep.value + 1, steps.length));
const prevStep = () => (currentStep.value = Math.max(currentStep.value - 1, 1));
</script>

<template>
  <AppShell>
    <PageHeader
      eyebrow="신규 사전진단 메인 플로우"
      :title="currentTitle"
      description="IA 기준 4단계 흐름을 mock 데이터로 구현했습니다."
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
      </aside>

      <div class="grid">
        <section v-if="currentStep === 1" class="result-layout">
          <div class="panel">
            <ParcelMapMock />
            <div class="notice" style="margin-top: 12px">
              공공데이터 조회 상태: 정상 · 기준일자 2025-05-20
            </div>
          </div>
          <div class="grid">
            <div class="panel">
              <div class="section-title"><h2>검색 방식</h2><span class="badge">주소</span></div>
              <div class="field"><label>주소 / 지번 / 좌표</label><input class="input" value="서울특별시 강남구 테헤란로 123" /></div>
              <ul class="mini-list" style="margin-top: 12px">
                <li><span>41287-10123-0123456</span><span class="badge">선택</span></li>
                <li><span>41287-10123-0123457</span><span class="badge neutral">후보</span></li>
                <li><span>41287-10123-0123458</span><span class="badge neutral">후보</span></li>
              </ul>
            </div>
            <div class="panel">
              <h2>선택된 대지 정보</h2>
              <table class="table">
                <tbody>
                  <tr><th>표준주소</th><td>서울특별시 강남구 테헤란로 123</td></tr>
                  <tr><th>지번</th><td>역삼동 123-45</td></tr>
                  <tr><th>법정동코드</th><td>1168051000</td></tr>
                  <tr><th>PNU</th><td>41287-10123-0123456</td></tr>
                  <tr><th>지목/면적</th><td>대 · 540.00㎡</td></tr>
                </tbody>
              </table>
            </div>
          </div>
        </section>

        <section v-else-if="currentStep === 2" class="grid two">
          <div class="panel">
            <div class="section-title"><h2>건축 계획 입력</h2><span class="badge">필수 정보</span></div>
            <div class="form-grid">
              <div class="field"><label>행위 유형</label><select class="select"><option>신축</option></select></div>
              <div class="field"><label>현재 용도</label><select class="select"><option>기존 건축물 없음</option></select></div>
              <div class="field"><label>희망 용도</label><select class="select"><option>업무시설</option></select></div>
              <div class="field"><label>대지 면적</label><input class="input" value="540.00 ㎡" /></div>
              <div class="field"><label>연면적</label><input class="input" value="1,200.00 ㎡" /></div>
              <div class="field"><label>층수</label><input class="input" value="5층" /></div>
            </div>
          </div>
          <div class="grid">
            <section class="panel">
              <h2>법률 판단용 문장</h2>
              <p>신축 행위를 위한 건축 계획입니다. 대지면적 540.00㎡, 연면적 1,200.00㎡, 지상 5층 업무시설을 계획합니다.</p>
            </section>
            <section class="panel">
              <h2>Action JSON 요약</h2>
              <pre class="code-block">{
  "actionType": "신축",
  "desiredUse": "업무시설",
  "siteArea": 540,
  "totalFloorArea": 1200,
  "floorCount": 5
}</pre>
            </section>
          </div>
        </section>

        <section v-else-if="currentStep === 3" class="grid">
          <div class="grid four">
            <div class="card"><span class="subtle">종합 판정</span><h2>조건부 가능성</h2></div>
            <div class="card"><span class="subtle">주 인허가 유형</span><h2>건축허가</h2></div>
            <div class="card"><span class="subtle">리스크 레벨</span><h2>중간</h2></div>
            <div class="card"><span class="subtle">누락정보</span><h2>3건</h2></div>
          </div>
          <section class="result-layout">
            <div class="panel">
              <div class="section-title"><h2>조건부 절차 목록</h2><span class="badge warning">관할부서 확인 필요</span></div>
              <table class="table">
                <thead><tr><th>절차명</th><th>대상 여부</th><th>판단 사유</th><th>담당 부서</th></tr></thead>
                <tbody>
                  <tr v-for="row in procedureRows" :key="row.name">
                    <td>{{ row.name }}</td><td>{{ row.target }}</td><td>{{ row.reason }}</td><td>{{ row.department }}</td>
                  </tr>
                </tbody>
              </table>
            </div>
            <EvidencePanel />
          </section>
          <section class="panel">
            <div class="section-title"><h2>추가 검토 항목 / 누락정보</h2><span class="badge warning">{{ missingItems.length }}건</span></div>
            <ul class="mini-list"><li v-for="item in missingItems" :key="item"><span>{{ item }}</span><span class="badge warning">우선순위 중간</span></li></ul>
            <div class="topbar-actions" style="margin-top: 14px">
              <RouterLink class="button" to="/projects/demo/diagnosis/alternatives"><AlertTriangle />대안 시나리오 보기</RouterLink>
              <button class="button primary" @click="currentStep = 4"><FileText />보고서 생성으로 이동</button>
            </div>
          </section>
        </section>

        <section v-else class="result-layout">
          <div class="grid">
            <section class="panel">
              <div class="section-title"><h2>생성할 실무 산출물</h2><span class="badge">5개 선택</span></div>
              <ul class="mini-list">
                <li><label><input type="checkbox" checked /> 체크리스트</label></li>
                <li><label><input type="checkbox" checked /> 필요서류 목록</label></li>
                <li><label><input type="checkbox" checked /> 부서별 사전협의 질문</label></li>
                <li><label><input type="checkbox" checked /> 신청서 / 신고서 초안</label></li>
                <li><label><input type="checkbox" checked /> 종합 보고서</label></li>
              </ul>
            </section>
            <section class="panel">
              <h2>중요 안내</h2>
              <p>모든 산출물은 사전진단 참고자료입니다. 최종 인허가 결정은 관할기관 검토와 최신 법령 적용에 따라 달라질 수 있습니다.</p>
              <div class="topbar-actions"><button class="button"><FileText />미리보기</button><button class="button primary"><Play />생성하기</button></div>
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
