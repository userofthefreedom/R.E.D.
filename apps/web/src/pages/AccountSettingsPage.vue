<script setup lang="ts">
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
</script>

<template>
  <AppShell>
    <PageHeader eyebrow="글로벌 / 계정" title="마이페이지 및 계정설정" description="프로필, 조직, 알림, 보안 설정을 관리합니다." />
    <section class="grid two">
      <div class="panel"><h2>프로필</h2><div class="grid"><div class="field"><label>이름</label><input class="input" value="홍길동" /></div><div class="field"><label>소속</label><input class="input" value="OO 시행사" /></div><div class="field"><label>역할</label><select class="select"><option>PM / 개발사업 실무자</option></select></div></div></div>
      <div class="panel"><h2>알림 설정</h2><ul class="mini-list"><li><label><input type="checkbox" checked /> 진단 완료 알림</label></li><li><label><input type="checkbox" checked /> 보고서 생성 알림</label></li><li><label><input type="checkbox" /> 법령 기준일자 변경 알림</label></li></ul></div>
    </section>
  </AppShell>
</template>
