<script setup lang="ts">
import { Bell } from "@lucide/vue";
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
</script>

<template>
  <AppShell>
    <PageHeader eyebrow="글로벌 / 알림" title="알림 및 최근 진단" description="진단 완료, 보완 필요, 보고서 생성 상태를 확인합니다." />
    <section class="panel">
      <ul class="mini-list">
        <li><span><Bell /> 강남 역삼동 근린시설 계획 진단이 완료되었습니다.</span><span class="badge">방금</span></li>
        <li><span>주차대수 변경 여부 입력이 필요합니다.</span><span class="badge warning">보완</span></li>
        <li><span>부산 해운대 업무시설 보고서 v1.0 생성 완료</span><span class="badge neutral">어제</span></li>
      </ul>
    </section>
  </AppShell>
</template>
