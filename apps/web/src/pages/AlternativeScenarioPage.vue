<script setup lang="ts">
import { ArrowLeft, FileCheck2, Lightbulb } from "@lucide/vue";
import { alternativeRows, diagnosisSummary, procedureRows, similarCases } from "../app/mockData";
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
</script>

<template>
  <AppShell>
    <PageHeader
      eyebrow="3-1 서브 페이지"
      title="대안 시나리오 탐색"
      description="저가능성 또는 고위험 판단일 때 결과 화면에서 분기되는 보조 의사결정 화면입니다."
    >
      <template #actions>
        <RouterLink class="button" to="/projects/demo/diagnosis"><ArrowLeft />결과 화면으로 복귀</RouterLink>
      </template>
    </PageHeader>

    <section class="grid two">
      <div class="panel">
        <div class="section-title"><h2>현재 판단 요약</h2><span class="badge warning">{{ diagnosisSummary.overall }}</span></div>
        <div class="grid three">
          <div class="card"><span class="subtle">주 인허가</span><h2>{{ diagnosisSummary.mainPermitType }}</h2></div>
          <div class="card"><span class="subtle">리스크</span><h2>{{ diagnosisSummary.riskLevel }}</h2></div>
          <div class="card"><span class="subtle">누락정보</span><h2>{{ diagnosisSummary.missingInfoCount }}건</h2></div>
        </div>
        <ul class="mini-list" style="margin-top: 14px">
          <li v-for="row in procedureRows.filter((item) => item.risk !== '낮음').slice(0, 3)" :key="row.name">
            <span><strong>{{ row.name }}</strong><br /><span class="subtle">{{ row.reason }}</span></span>
            <span class="badge warning">{{ row.risk }}</span>
          </li>
        </ul>
      </div>

      <div class="notice action-recommendation">
        <Lightbulb />
        <h2>권장 다음 행동</h2>
        <p>현재 입력 기준으로는 주차계획 보완안을 우선 검토하는 흐름이 가장 안정적입니다.</p>
        <ol class="action-steps">
          <li><strong>1. 주차계획 보완안 선택</strong><span>변경 후 주차대수 12대 기준으로 조례 리스크를 낮춥니다.</span></li>
          <li><strong>2. 교통과 사전협의 질문 생성</strong><span>부설주차장 산정 기준, 기계식 주차 가능성, 추가 자료를 확인합니다.</span></li>
          <li><strong>3. 건축과 제출자료 후보 반영</strong><span>배치도, 주차계획도, 도로 접도 확인자료를 보고서에 추가합니다.</span></li>
        </ol>
        <div class="topbar-actions">
          <button class="button">사전협의 질문 생성</button>
          <button class="button primary"><FileCheck2 />보고서에 반영</button>
        </div>
      </div>
    </section>

    <section class="panel" style="margin-top: 18px">
      <div class="section-title"><h2>유사 인허가 사례</h2><span class="badge">참고사례</span></div>
      <div class="grid two">
        <article v-for="item in similarCases" :key="item.title" class="trace-card">
          <div class="section-title compact">
            <strong>{{ item.title }}</strong>
            <span class="badge">{{ item.similarity }}%</span>
          </div>
          <p>{{ item.referencePoint }}</p>
          <div class="trace-meta">
            <span>{{ item.region }} · {{ item.useDistrict }}</span>
            <span>{{ item.landCategory }} · {{ item.result }}</span>
          </div>
        </article>
      </div>
    </section>

    <section class="panel" style="margin-top: 18px">
      <div class="section-title"><h2>대안 비교</h2><span class="badge">{{ alternativeRows.length }}개 후보</span></div>
      <table class="table">
        <thead><tr><th>대안</th><th>기대효과</th><th>한계</th><th>협의 포인트</th><th>우선도</th></tr></thead>
        <tbody>
          <tr v-for="row in alternativeRows" :key="row.name">
            <td>{{ row.name }}</td>
            <td>{{ row.effect }}</td>
            <td>{{ row.limit }}</td>
            <td>{{ row.consultation }}</td>
            <td><span class="badge">{{ row.score }}점</span></td>
          </tr>
        </tbody>
      </table>
      <div class="topbar-actions" style="margin-top: 14px">
        <button class="button">대안별 리스크 재검토</button>
        <button class="button primary"><FileCheck2 />선택 대안 보고서 반영</button>
      </div>
    </section>
  </AppShell>
</template>
