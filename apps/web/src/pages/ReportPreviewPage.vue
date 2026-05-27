<script setup lang="ts">
import { Download, FileArchive, Play } from "@lucide/vue";
import { savedReports } from "../app/mockData";
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
import ReportPreviewMock from "../components/report/ReportPreviewMock.vue";
</script>

<template>
  <AppShell>
    <PageHeader eyebrow="실무 산출물 생성" title="보고서 미리보기" description="체크리스트, 필요서류, 사전협의 질문, 신청서 초안, 종합보고서를 검토합니다.">
      <template #actions><button class="button"><Download />PDF</button><button class="button primary"><FileArchive />DOCX</button></template>
    </PageHeader>
    <section class="result-layout">
      <div class="grid">
        <div class="panel"><div class="section-title"><h2>생성 항목</h2><span class="badge">선택됨</span></div><ul class="mini-list"><li v-for="report in savedReports" :key="report"><span>{{ report }}</span><span class="badge">v1.0</span></li></ul></div>
        <div class="panel"><h2>프로젝트 요약</h2><p>신축 · 업무시설 · 대지 540.00㎡ · 연면적 1,200.00㎡ · 조건부 가능성 · 주 인허가 유형 건축허가</p><button class="button primary"><Play />생성하기</button></div>
      </div>
      <ReportPreviewMock />
    </section>
  </AppShell>
</template>
