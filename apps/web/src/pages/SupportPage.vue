<script setup lang="ts">
import { AlertTriangle, HelpCircle, Info, Users } from "@lucide/vue";
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
</script>

<template>
  <AppShell>
    <PageHeader eyebrow="지원 / 예외 안내" title="고객지원 및 보조 화면" description="조회 실패, 보완 요청, 사전협의 안내를 상황별로 정리합니다." />
    <section class="grid four">
      <div class="panel"><AlertTriangle /><h2>공공데이터 조회 실패</h2><p>실패 사유와 재시도, 대체 입력, 관리자 문의 동선을 제공합니다.</p><button class="button">다시 시도</button></div>
      <div class="panel"><Info /><h2>추가정보 필요</h2><p>누락된 입력 항목과 보완 가이드를 안내합니다.</p><button class="button">정보 입력하기</button></div>
      <div class="panel"><Users /><h2>관할부서 사전협의</h2><p>협의 필요 사유, 담당부서 후보, 문의 템플릿을 제공합니다.</p><button class="button">관련 부서 보기</button></div>
      <div class="panel"><HelpCircle /><h2>결과 없음 / 오류</h2><p>입력 확인, 다시 시도, 고객센터 문의 경로를 제공합니다.</p><button class="button">문의하기</button></div>
    </section>
  </AppShell>
</template>
