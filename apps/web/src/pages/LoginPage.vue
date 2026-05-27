<script setup lang="ts">
import { LogIn } from "@lucide/vue";
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
</script>

<template>
  <AppShell>
    <PageHeader eyebrow="글로벌 / 인증" title="로그인" description="기존 프로젝트와 저장 보고서에 접근합니다." />
    <section class="split-layout">
      <form class="panel">
        <div class="grid">
          <div class="field"><label>이메일 또는 아이디</label><input class="input" value="demo@permit.ai" /></div>
          <div class="field"><label>비밀번호</label><input class="input" type="password" value="password" /></div>
          <label><input type="checkbox" checked /> 로그인 상태 유지</label>
          <RouterLink class="button primary" to="/dashboard"><LogIn />로그인</RouterLink>
        </div>
      </form>
      <div class="notice">
        <h2>소셜 로그인</h2>
        <p>업무 계정과 개인 계정을 모두 고려한 로그인 영역입니다. 실제 연동은 추후 인증 설계에 맞춰 붙입니다.</p>
        <div class="grid three"><button class="button">G</button><button class="button">N</button><button class="button">Apple</button></div>
      </div>
    </section>
  </AppShell>
</template>
