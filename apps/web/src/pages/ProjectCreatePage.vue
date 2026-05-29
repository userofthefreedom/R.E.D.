<script setup lang="ts">
import { ArrowRight, CheckCircle2, ClipboardList, FilePlus2, MapPinned, ShieldCheck } from "@lucide/vue";
import { ref } from "vue";
import { useRouter } from "vue-router";
import { createProject } from "../api/project.api";
import { projectRows } from "../app/mockData";
import PageHeader from "../components/common/PageHeader.vue";
import AppShell from "../components/layout/AppShell.vue";
import { useProjectStore } from "../stores/project.store";

const router = useRouter();
const projectStore = useProjectStore();
const isCreating = ref(false);

async function startDiagnosis() {
  const prototypeProject = projectRows[0];
  isCreating.value = true;
  try {
    const project = await createProject({
      name: prototypeProject.name,
      address: prototypeProject.address,
      pnu: prototypeProject.pnu,
      description: "prototype diagnosis workspace",
    });
    projectStore.currentProjectId = project.id;
    projectStore.currentParcelId = null;
    projectStore.currentRegulationOverlayId = null;
    projectStore.currentActionId = null;
    projectStore.currentDiagnosisRunId = null;
  } finally {
    isCreating.value = false;
    await router.push("/projects/demo/diagnosis");
  }
}
</script>

<template>
  <AppShell>
    <PageHeader
      eyebrow="신규 사전진단"
      title="새 진단 시작"
      description="프로젝트 정보를 만들고, 위치 확인부터 산출물 생성까지 한 번에 이어지는 4단계 진단을 시작합니다."
    />

    <section class="create-layout">
      <div class="panel">
        <div class="section-title">
          <div>
            <h2>프로젝트 기본 정보</h2>
            <p class="subtle">회의용 프로토타입에서는 아래 값으로 바로 진단 흐름에 진입합니다.</p>
          </div>
          <FilePlus2 />
        </div>
        <div class="grid">
          <div class="field"><label>프로젝트명</label><input class="input" value="강남 역삼동 근린시설 계획" /></div>
          <div class="field"><label>검토 목적</label><select class="select"><option>토지매입 전 사전검토</option></select></div>
          <div class="field"><label>대상 지역</label><input class="input" value="서울특별시 강남구 역삼동" /></div>
          <div class="field"><label>희망 건축행위</label><select class="select"><option>신축 · 업무시설</option></select></div>
          <div class="field"><label>메모</label><textarea class="textarea">신축 가능성과 조건부 절차를 우선 확인합니다.</textarea></div>
          <button class="button primary" type="button" :disabled="isCreating" @click="startDiagnosis"><ArrowRight />진단 흐름으로 이동</button>
        </div>
      </div>

      <div class="grid">
        <section class="panel">
          <div class="section-title"><h2>이번 진단에서 확인할 항목</h2><span class="badge">4단계</span></div>
          <div class="flow-strip">
            <div class="flow-step"><MapPinned /><strong>1. 위치</strong><span class="subtle">주소/PNU/필지 Polygon</span></div>
            <div class="flow-step"><ClipboardList /><strong>2. 계획</strong><span class="subtle">Action JSON 정규화</span></div>
            <div class="flow-step"><ShieldCheck /><strong>3. 판정</strong><span class="subtle">Rule/Evidence Trace</span></div>
            <div class="flow-step"><FilePlus2 /><strong>4. 산출물</strong><span class="subtle">체크리스트/DOCX/PDF</span></div>
          </div>
        </section>

        <section class="grid three">
          <article class="card">
            <CheckCircle2 />
            <h3>입력 누락 사전 검증</h3>
            <p>주차대수, 도로 폭, 성토/절토 같은 판단 필수값을 진단 전 점검합니다.</p>
          </article>
          <article class="card">
            <CheckCircle2 />
            <h3>근거 기준일 표시</h3>
            <p>공공데이터 기준일과 법령 기준일을 결과와 보고서에 함께 남깁니다.</p>
          </article>
          <article class="card">
            <CheckCircle2 />
            <h3>사전협의 질문 생성</h3>
            <p>조건부 절차별 담당부서에 확인할 질문을 산출물로 이어갑니다.</p>
          </article>
        </section>

        <section class="panel">
          <div class="section-title"><h2>시작 전 확인</h2><span class="badge warning">Mock data</span></div>
          <ul class="mini-list">
            <li><span>실제 API 호출 전 화면 흐름 검증용 데이터가 사용됩니다.</span><span class="badge neutral">프로토타입</span></li>
            <li><span>외부 API 키는 루트 `.env`에만 저장하며 브라우저에 노출하지 않습니다.</span><span class="badge">보안</span></li>
            <li><span>결과는 확정 판정이 아니라 사전진단 참고자료로 표시됩니다.</span><span class="badge warning">주의</span></li>
          </ul>
        </section>
      </div>
    </section>
  </AppShell>
</template>
