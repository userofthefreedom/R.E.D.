<script setup lang="ts">
import { UserPlus } from "@lucide/vue";
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
</script>

<template>
  <AppShell>
    <PageHeader eyebrow="글로벌 / 인증" title="회원가입" description="이름, 이메일, 조직 정보를 입력하고 약관에 동의합니다." />
    <form class="panel" style="max-width: 720px">
      <div class="form-grid">
        <div class="field"><label>이름</label><input class="input" value="홍길동" /></div>
        <div class="field"><label>이메일</label><input class="input" value="user@example.com" /></div>
        <div class="field"><label>비밀번호</label><input class="input" type="password" value="password" /></div>
        <div class="field"><label>비밀번호 확인</label><input class="input" type="password" value="password" /></div>
        <div class="field"><label>소속</label><input class="input" value="OO 시행사" /></div>
        <div class="field"><label>역할</label><select class="select"><option>개발사업 실무자</option></select></div>
      </div>
      <div class="topbar-actions" style="margin-top: 16px">
        <label><input type="checkbox" checked /> 이용약관 동의</label>
        <RouterLink class="button primary" to="/dashboard"><UserPlus />회원가입</RouterLink>
      </div>
    </form>
  </AppShell>
</template>
