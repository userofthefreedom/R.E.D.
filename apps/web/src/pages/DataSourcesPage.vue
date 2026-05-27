<script setup lang="ts">
import { dataSourceRows } from "../app/mockData";
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
</script>

<template>
  <AppShell>
    <PageHeader eyebrow="글로벌 / 데이터 출처" title="데이터 출처 및 면책 안내" description="진단 결과의 기준일자, 수집 시각, 최종 판단 주체를 명확하게 안내합니다." />
    <section class="panel">
      <table class="table">
        <thead><tr><th>영역</th><th>출처</th><th>관리 방식</th></tr></thead>
        <tbody><tr v-for="row in dataSourceRows" :key="row[0]"><td>{{ row[0] }}</td><td>{{ row[1] }}</td><td>{{ row[2] }}</td></tr></tbody>
      </table>
    </section>
    <section class="notice" style="margin-top: 18px">
      본 서비스의 결과는 AI 기반 사전진단 참고자료입니다. 최종 인허가 여부는 관할 행정청의 검토와 최신 법령·조례 적용에 따라 결정됩니다.
    </section>
  </AppShell>
</template>
