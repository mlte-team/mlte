<template>
  <NuxtLayout name="base-layout">
    <title>Negotiation Card</title>
    <template #page-title>Negotiation Card</template>
    <UsaTextInput
      v-if="queryArtifactId === undefined"
      v-model="userInputArtifactId"
      :error="formErrors.identifier"
    >
      <template #label>
        Artifact ID
        <TemplatesTooltipInfo>
          The Artifact ID this negotiation card <br />
          will be saved under upon submission.
        </TemplatesTooltipInfo>
      </template>
      <template #error-message> Identifier cannot be empty </template>
    </UsaTextInput>
    <div v-else>
      <TemplatesArtifactInfo
        :id="queryArtifactId as string"
        :model="queryModel as string"
        :version="queryVersion as string"
        :creator="creator"
        :timestamp="timestamp"
      />
    </div>

    <p>
      Teams should use the negotiation card to guide an in-depth discussion for
      project scoping. The card can be completed in any order and the idea is
      that teams fill out as much as they can at the beginning of the project
      process and revisit the card throughout as the project matures. There are
      four sections in the Negotiation Card:
    </p>
    <ul>
      <li>System Information</li>
      <li>Data</li>
      <li>Model Information</li>
      <li>System Requirements</li>
    </ul>
    <p>
      Negotiation Cards serve as a critical reference for teams throughout
      development even when they are partially filled out. Hover over the black
      information icons next to each field to get more information about that
      field. Click on the Example button to see specific examples for a section.
    </p>

    <CardSystemInformation ref="systemInformationRef" v-model="form.system" />

    <CardDataFields ref="dataRef" v-model="form.data" />

    <CardModelFields ref="modelRef" v-model="form.model" />

    <CardSystemRequirements v-model="form.system_requirements" />

    <div class="submit-footer">
      <UsaButton class="primary-button" @click="cancelFormSubmission('/')">
        Cancel
      </UsaButton>
      <UsaButton class="primary-button" @click="submit()"> Save </UsaButton>
    </div>
  </NuxtLayout>
</template>

<script setup lang="ts">
import { cancelFormSubmission } from "~/app/composables/form-methods";
import { provide } from "vue";

const queryModel = useRoute().query.model;
const queryVersion = useRoute().query.version;
const queryArtifactId = useRoute().query.artifactId;
const forceSaveParam = ref(useRoute().query.artifactId !== undefined);
// References to child components used to call their methods when importing descriptors
const systemInformationRef = ref(null);
const dataRef = ref(null);
const modelRef = ref(null);

const userInputArtifactId = ref("default");
const creator = ref("");
const timestamp = ref("");
const form = ref(new NegotiationCardModel());
const formErrors = ref<Dictionary<boolean>>({
  identifier: false,
  problem_type: false,
  classification: false,
  qa: false,
});

provide("formErrors", formErrors);

await updateCardCustomLists();
if (queryArtifactId !== undefined) {
  const card = await getCard(
    queryModel as string,
    queryVersion as string,
    queryArtifactId as string,
  );
  if (card) {
    creator.value = card.header.creator;
    timestamp.value = timestampToString(card.header.timestamp);
    form.value = card.body;
  }
}

// Handle submission of form.
async function submit() {
  const identifier = (queryArtifactId as string) || userInputArtifactId.value;
  formErrors.value = resetFormErrors(formErrors.value);
  let inputError = false;

  if (identifier === "") {
    formErrors.value.identifier = true;
    inputError = true;
  }

  if (form.value.system.problem_type === "Other") {
    formErrors.value.problem_type = true;
    inputError = true;
  }

  form.value.data.forEach((dataDescriptor: DataDescriptor) => {
    if (dataDescriptor.classification === "Other") {
      formErrors.value.classification = true;
      inputError = true;
    }
  });

  form.value.system_requirements.forEach((requirement: QASDescriptor) => {
    if (requirement.quality === "Other") {
      formErrors.value.qa = true;
      inputError = true;
    }
  });

  if (inputError) {
    inputErrorAlert();
    return;
  }

  const response = await saveCard(
    queryModel as string,
    queryVersion as string,
    identifier,
    forceSaveParam.value,
    form.value,
  );
  if (response) {
    forceSaveParam.value = true;
    if (useRoute().query.artifactId === undefined) {
      window.location.href =
        "/artifact/negotiation-card?" +
        "model=" +
        useRoute().query.model +
        "&version=" +
        useRoute().query.version +
        "&artifactId=card." +
        identifier;
    } else {
      response.body.system_requirements.forEach(
        (requirement: QASDescriptor, index: number) => {
          form.value.system_requirements[index].identifier =
            requirement.identifier;
        },
      );
    }
  }
}
</script>
