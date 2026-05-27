<script setup lang="ts">
import { FileText, MapPinned, Scale, ShieldCheck } from "@lucide/vue";
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
</script>

<template>
  <AppShell>
    <PageHeader eyebrow="글로벌 / 서비스 소개" title="서비스 소개" description="단순 법령 검색이 아니라 위치, 행위, 규칙, 근거, 보고서를 연결하는 사전진단 플랫폼입니다." />
    <section class="grid four">
      <div class="card"><MapPinned /><h2>위치 기반 진단</h2><p>PNU와 필지 Geometry 중심으로 판단합니다.</p></div>
      <div class="card"><Scale /><h2>룰엔진 판단</h2><p>LLM이 아니라 규칙 기반으로 절차 후보를 만듭니다.</p></div>
      <div class="card"><ShieldCheck /><h2>근거 추적</h2><p>Rule Trace와 Evidence Trace를 함께 남깁니다.</p></div>
      <div class="card"><FileText /><h2>산출물 생성</h2><p>체크리스트와 보고서를 실무 형태로 만듭니다.</p></div>
    </section>
  </AppShell>
</template>
