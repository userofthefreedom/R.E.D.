<script setup lang="ts">
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
</script>

<template>
  <AppShell>
    <PageHeader eyebrow="프로젝트 / 진단 이력" title="진단 이력 및 버전 비교" description="두 번의 진단 실행을 선택해 판정, 조건부 절차, 리스크, 근거 변경을 비교합니다." />
    <section class="snapshot-row">
      <div class="panel"><h2>비교 기준</h2><p>진단 실행 v1 · 2025-05-18 14:28</p><ul><li>종합 판정: 적합</li><li>조건부/보완: 2건</li><li>리스크: 1건</li></ul></div>
      <div class="panel"><h2>비교 결과 요약</h2><ul><li>변경된 항목 수: 7건</li><li>추가된 조건부: +1건</li><li>추가된 리스크: +1건</li></ul></div>
      <div class="panel"><h2>비교 대상</h2><p>진단 실행 v2 · 2025-05-20 11:05</p><ul><li>종합 판정: 적합(조건부)</li><li>조건부/보완: 3건</li><li>리스크: 2건</li></ul></div>
    </section>
    <section class="grid two" style="margin-top: 18px">
      <div class="panel"><h2>변경된 규칙 / 기준</h2><table class="table"><thead><tr><th>구분</th><th>항목</th><th>이전</th><th>현재</th><th>변경 내용</th></tr></thead><tbody><tr><td>법령</td><td>건축법 제11조</td><td>O</td><td>X</td><td>적용 제외 조건 반영</td></tr></tbody></table></div>
      <div class="panel"><h2>변경된 근거</h2><table class="table"><thead><tr><th>구분</th><th>근거명</th><th>이전 링크</th><th>현재 링크</th><th>변경 내용</th></tr></thead><tbody><tr><td>법령</td><td>건축법 제11조</td><td>링크 A</td><td>링크 B</td><td>조문 개정 반영</td></tr></tbody></table></div>
    </section>
  </AppShell>
</template>
