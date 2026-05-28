<script setup lang="ts">
import { Download, FileText, Maximize, Search, ZoomIn } from "@lucide/vue";
import { diagnosisMeta, procedureRows, selectedParcel } from "../../app/mockData";
</script>

<template>
  <section class="panel report-preview">
    <div class="preview-toolbar">
      <div class="topbar-actions">
        <button class="button ghost" title="페이지">1 / 15</button>
        <button class="button ghost" title="확대"><ZoomIn />100%</button>
      </div>
      <div class="topbar-actions">
        <button class="button ghost" title="검색"><Search /></button>
        <button class="button ghost" title="DOCX 다운로드"><FileText />DOCX</button>
        <button class="button ghost" title="PDF 다운로드"><Download />PDF</button>
        <button class="button ghost" title="전체화면"><Maximize /></button>
      </div>
    </div>
    <div class="document-page">
      <p class="eyebrow">R.E.D. 사전진단 보고서</p>
      <h2>건축 인허가 사전진단 종합보고서</h2>
      <p>대상지: {{ selectedParcel.standardAddress }} · PNU {{ selectedParcel.pnu }}</p>

      <div class="report-summary-grid">
        <div>
          <span class="subtle">종합 판정</span>
          <strong>조건부 가능성</strong>
        </div>
        <div>
          <span class="subtle">주 인허가</span>
          <strong>건축허가</strong>
        </div>
        <div>
          <span class="subtle">리스크</span>
          <strong>중간</strong>
        </div>
      </div>

      <h3>조건부 절차 요약</h3>
      <ol class="report-list">
        <li v-for="row in procedureRows.slice(0, 4)" :key="row.name">
          <strong>{{ row.name }}</strong>
          <span>{{ row.target }} · {{ row.department }}</span>
        </li>
      </ol>

      <div class="report-footnote">
        기준일자 {{ diagnosisMeta.dataBaseDate }} · 적용 룰셋 {{ diagnosisMeta.ruleSetVersion }} ·
        모든 산출물은 사전진단 참고자료입니다.
      </div>
    </div>
  </section>
</template>
