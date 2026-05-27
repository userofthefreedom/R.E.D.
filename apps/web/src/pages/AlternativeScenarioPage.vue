<script setup lang="ts">
import { ArrowLeft, FileCheck2, Lightbulb } from "@lucide/vue";
import { alternativeRows } from "../app/mockData";
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
</script>

<template>
  <AppShell>
    <PageHeader eyebrow="3-1 서브 페이지" title="대안 시나리오 탐색" description="저가능성 또는 고위험 판정일 때 결과 화면에서 분기되는 보조 의사결정 화면입니다.">
      <template #actions><RouterLink class="button" to="/projects/demo/diagnosis"><ArrowLeft />결과 화면으로 복귀</RouterLink></template>
    </PageHeader>
    <section class="grid two">
      <div class="panel">
        <div class="section-title"><h2>리스크 원인 분석</h2><span class="badge warning">조건부 가능성</span></div>
        <ul><li>희망 용도가 지구단위계획상 제한될 가능성이 있습니다.</li><li>주차 기준 증가 가능성이 있어 추가 검토가 필요합니다.</li><li>성토/절토 규모 미입력으로 개발행위허가 판단이 보류되었습니다.</li></ul>
      </div>
      <div class="notice"><Lightbulb /><h2>의사결정 메모</h2><p>선택한 대안은 보고서에 반영되어 내부 보고와 사전협의 자료로 이어집니다.</p></div>
    </section>
    <section class="panel" style="margin-top: 18px">
      <div class="section-title"><h2>대안 비교</h2><span class="badge">3개 후보</span></div>
      <table class="table">
        <thead><tr><th>대안</th><th>기대효과</th><th>한계</th><th>협의 포인트</th></tr></thead>
        <tbody><tr v-for="row in alternativeRows" :key="row.name"><td>{{ row.name }}</td><td>{{ row.effect }}</td><td>{{ row.limit }}</td><td>{{ row.consultation }}</td></tr></tbody>
      </table>
      <div class="topbar-actions" style="margin-top: 14px"><button class="button primary"><FileCheck2 />보고서에 반영</button></div>
    </section>
  </AppShell>
</template>
