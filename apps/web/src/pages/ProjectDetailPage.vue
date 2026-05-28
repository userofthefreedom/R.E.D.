<script setup lang="ts">
import { Download, History, PenLine } from "@lucide/vue";
import { actionJson, diagnosisMeta, diagnosisSummary, savedReports, selectedParcel } from "../app/mockData";
import EvidencePanel from "../components/evidence/EvidencePanel.vue";
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
</script>

<template>
  <AppShell>
    <PageHeader
      eyebrow="프로젝트 / 상세"
      title="강남 역삼동 근린시설 계획"
      description="프로젝트 기본 정보, 진단 요약, 저장 보고서, 근거 스냅샷, Action 이력을 확인합니다."
    >
      <template #actions>
        <RouterLink class="button" to="/projects/demo/history"><History />이력 비교</RouterLink>
        <RouterLink class="button primary" to="/projects/demo/diagnosis"><PenLine />진단 수정</RouterLink>
      </template>
    </PageHeader>

    <section class="grid four">
      <div class="card"><span class="subtle">종합 판정</span><h2>{{ diagnosisSummary.overall }}</h2><span class="badge warning">사전협의 권장</span></div>
      <div class="card"><span class="subtle">주 인허가 유형</span><h2>{{ diagnosisSummary.mainPermitType }}</h2></div>
      <div class="card"><span class="subtle">조건부/보완</span><h2>{{ diagnosisSummary.missingInfoCount }}건</h2></div>
      <div class="card"><span class="subtle">근거 버전</span><h2>v0.1.0</h2></div>
    </section>

    <section class="grid two" style="margin-top: 18px">
      <div class="panel">
        <h2>대상지 정보</h2>
        <table class="table">
          <tbody>
            <tr><th>표준주소</th><td>{{ selectedParcel.standardAddress }}</td></tr>
            <tr><th>지번</th><td>{{ selectedParcel.jibunAddress }}</td></tr>
            <tr><th>PNU</th><td>{{ selectedParcel.pnu }}</td></tr>
            <tr><th>용도지역</th><td>{{ selectedParcel.useDistrict }}</td></tr>
            <tr><th>기준일자</th><td>{{ selectedParcel.dataBaseDate }}</td></tr>
          </tbody>
        </table>
      </div>
      <div class="panel">
        <div class="section-title"><h2>저장된 보고서</h2><button class="button"><Download />모두 다운로드</button></div>
        <ul class="mini-list">
          <li v-for="report in savedReports" :key="report">
            <span>{{ report }}<br /><span class="subtle">{{ diagnosisMeta.ruleSetVersion }} · {{ diagnosisMeta.lawBaseDate }}</span></span>
            <button class="button"><Download />다운로드</button>
          </li>
        </ul>
      </div>
    </section>

    <section class="grid two" style="margin-top: 18px">
      <div class="panel">
        <h2>Action 이력 / 현재 입력 스냅샷</h2>
        <pre class="code-block">{{ JSON.stringify(actionJson, null, 2) }}</pre>
      </div>
      <div class="panel">
        <h2>근거 스냅샷</h2>
        <table class="table">
          <tbody>
            <tr><th>데이터 기준일</th><td>{{ diagnosisMeta.dataBaseDate }}</td></tr>
            <tr><th>법령 기준일</th><td>{{ diagnosisMeta.lawBaseDate }}</td></tr>
            <tr><th>룰셋</th><td>{{ diagnosisMeta.ruleSetVersion }}</td></tr>
            <tr><th>RAG 인덱스</th><td>{{ diagnosisMeta.ragIndexVersion }}</td></tr>
          </tbody>
        </table>
      </div>
    </section>

    <section style="margin-top: 18px"><EvidencePanel /></section>
  </AppShell>
</template>
