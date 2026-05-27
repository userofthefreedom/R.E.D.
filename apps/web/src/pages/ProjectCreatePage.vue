<script setup lang="ts">
import { ArrowRight, FilePlus2 } from "@lucide/vue";
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
</script>

<template>
  <AppShell>
    <PageHeader eyebrow="신규 사전진단" title="새 진단 시작" description="프로젝트 생성 후 곧바로 4단계 진단 흐름으로 이동합니다." />
    <section class="split-layout">
      <div class="panel">
        <div class="section-title"><h2>프로젝트 기본 정보</h2><FilePlus2 /></div>
        <div class="grid">
          <div class="field"><label>프로젝트명</label><input class="input" value="강남 역삼동 근린시설 계획" /></div>
          <div class="field"><label>검토 목적</label><select class="select"><option>토지매입 전 사전검토</option></select></div>
          <div class="field"><label>메모</label><textarea class="textarea">신축 가능성과 조건부 절차를 우선 확인합니다.</textarea></div>
          <RouterLink class="button primary" to="/projects/demo/diagnosis"><ArrowRight />진단 흐름으로 이동</RouterLink>
        </div>
      </div>
      <div class="panel">
        <h2>이번 진단에서 확인할 항목</h2>
        <div class="flow-strip" style="margin-top: 16px">
          <div class="flow-step"><strong>1. 위치</strong><span class="subtle">주소/PNU/필지</span></div>
          <div class="flow-step"><strong>2. 계획</strong><span class="subtle">Action JSON</span></div>
          <div class="flow-step"><strong>3. 판정</strong><span class="subtle">Rule/Evidence</span></div>
          <div class="flow-step"><strong>4. 산출물</strong><span class="subtle">DOCX/PDF</span></div>
        </div>
      </div>
    </section>
  </AppShell>
</template>
