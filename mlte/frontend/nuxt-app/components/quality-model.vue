<template>
  <div class="model-container">
    <div class="svg-scroll-container">
      <svg
        viewBox="0 0 1300 750"
        xmlns="http://www.w3.org/2000/svg"
        preserveAspectRatio="xMinYMin meet"
        class="interactive-diagram"
      >
        <path
          d="M 80 100 H 1190"
          stroke="#333"
          fill="none"
          stroke-width="1.5"
        />
        <line
          x1="725"
          y1="60"
          x2="725"
          y2="100"
          stroke="#333"
          stroke-width="1.5"
        />

        <g>
          <rect
            x="475"
            y="5"
            width="500"
            height="60"
            fill="#dae8fc"
            stroke="#6c8ebf"
            rx="5"
          />
          <text x="725" y="45" text-anchor="middle" class="txt-root">
            Quality Model for ML Components
          </text>
        </g>

        <line
          x1="80"
          y1="100"
          x2="80"
          y2="120"
          stroke="#333"
          stroke-width="1.5"
        />
        <g
          class="node"
          @mouseenter="setNode('cat-behavior')"
          @mouseleave="clearNode"
        >
          <rect
            x="0"
            y="120"
            width="160"
            height="50"
            fill="#e1d5e7"
            stroke="#9673a6"
            rx="4"
          />
          <text x="80" y="140" text-anchor="middle" class="txt-cat">
            <tspan x="80" dy="0">Behavior</tspan>
            <tspan x="80" dy="1.2em">Analysis</tspan>
          </text>
        </g>
        <path
          d="M 30 170 V 360 M 30 210 h 20 M 30 260 h 20 M 30 310 h 20 M 30 360 h 20"
          stroke="#333"
          fill="none"
        />
        <g
          class="node"
          @mouseenter="setNode('analyzability')"
          @mouseleave="clearNode"
        >
          <rect
            x="50"
            y="190"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="115" y="215" text-anchor="middle" class="txt-item">
            Analyzability
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('monitorability')"
          @mouseleave="clearNode"
        >
          <rect
            x="50"
            y="240"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="115" y="265" text-anchor="middle" class="txt-item">
            Monitorability
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('testability')"
          @mouseleave="clearNode"
        >
          <rect
            x="50"
            y="290"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="115" y="315" text-anchor="middle" class="txt-item">
            Testability
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('understandability')"
          @mouseleave="clearNode"
        >
          <rect
            x="50"
            y="340"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text
            x="115"
            y="365"
            text-anchor="middle"
            class="txt-item"
            @mouseleave="clearNode"
          >
            Understandability
          </text>
        </g>

        <line
          x1="270"
          y1="100"
          x2="270"
          y2="120"
          stroke="#333"
          stroke-width="1.5"
        />
        <g
          class="node"
          @mouseenter="setNode('cat-confidence')"
          @mouseleave="clearNode"
        >
          <rect
            x="190"
            y="120"
            width="160"
            height="50"
            fill="#e1d5e7"
            stroke="#9673a6"
            rx="4"
          />
          <text x="270" y="150" text-anchor="middle" class="txt-cat">
            Confidence
          </text>
        </g>
        <path
          d="M 210 170 V 315 M 210 210 h 20 M 210 265 h 20 M 210 315 h 20"
          stroke="#333"
          fill="none"
        />
        <g
          class="node"
          @mouseenter="setNode('explainability')"
          @mouseleave="clearNode"
        >
          <rect
            x="230"
            y="190"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="295" y="215" text-anchor="middle" class="txt-item">
            Explainability
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('functional-correctness')"
          @mouseleave="clearNode"
        >
          <rect
            x="230"
            y="240"
            width="130"
            height="50"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="295" y="260" text-anchor="middle" class="txt-item">
            <tspan x="295" dy="0">Functional</tspan>
            <tspan x="295" dy="1.2em">Correctness</tspan>
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('interpretability')"
          @mouseleave="clearNode"
        >
          <rect
            x="230"
            y="300"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="295" y="325" text-anchor="middle" class="txt-item">
            Interpretability
          </text>
        </g>

        <line
          x1="450"
          y1="100"
          x2="450"
          y2="120"
          stroke="#333"
          stroke-width="1.5"
        />
        <g
          class="node"
          @mouseenter="setNode('cat-consistency')"
          @mouseleave="clearNode"
        >
          <rect
            x="370"
            y="120"
            width="160"
            height="50"
            fill="#e1d5e7"
            stroke="#9673a6"
            rx="4"
          />
          <text x="450" y="150" text-anchor="middle" class="txt-cat">
            Consistency
          </text>
        </g>
        <path
          d="M 390 170 V 260 M 390 210 h 20 M 390 260 h 20"
          stroke="#333"
          fill="none"
        />
        <g
          class="node"
          @mouseenter="setNode('repeatability')"
          @mouseleave="clearNode"
        >
          <rect
            x="410"
            y="190"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="475" y="215" text-anchor="middle" class="txt-item">
            Repeatability
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('reproducibility')"
          @mouseleave="clearNode"
        >
          <rect
            x="410"
            y="240"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="475" y="265" text-anchor="middle" class="txt-item">
            Reproducibility
          </text>
        </g>

        <line
          x1="640"
          y1="100"
          x2="640"
          y2="120"
          stroke="#333"
          stroke-width="1.5"
        />
        <g
          class="node"
          @mouseenter="setNode('cat-operation')"
          @mouseleave="clearNode"
        >
          <rect
            x="560"
            y="120"
            width="160"
            height="50"
            fill="#e1d5e7"
            stroke="#9673a6"
            rx="4"
          />
          <text x="640" y="142" text-anchor="middle" class="txt-cat">
            <tspan x="640" dy="0">Continued</tspan>
            <tspan x="640" dy="1.2em">Operation</tspan>
          </text>
        </g>
        <path
          d="M 575 170 V 470 M 575 210 h 20 M 575 260 h 20 M 575 310 h 20 M 575 365 h 20 M 575 420 h 20 M 575 470 h 20"
          stroke="#333"
          fill="none"
        />
        <g
          class="node"
          @mouseenter="setNode('deployability')"
          @mouseleave="clearNode"
        >
          <rect
            x="595"
            y="190"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="660" y="215" text-anchor="middle" class="txt-item">
            Deployability
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('resilience')"
          @mouseleave="clearNode"
        >
          <rect
            x="595"
            y="240"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="660" y="265" text-anchor="middle" class="txt-item">
            Resilience
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('reliability')"
          @mouseleave="clearNode"
        >
          <rect
            x="595"
            y="290"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="660" y="315" text-anchor="middle" class="txt-item">
            Reliability
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('resource-utilization')"
          @mouseleave="clearNode"
        >
          <rect
            x="595"
            y="340"
            width="130"
            height="50"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="660" y="360" text-anchor="middle" class="txt-item">
            <tspan x="660" dy="0">Resource</tspan>
            <tspan x="660" dy="1.2em">Utilization</tspan>
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('robustness')"
          @mouseleave="clearNode"
        >
          <rect
            x="595"
            y="400"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="660" y="425" text-anchor="middle" class="txt-item">
            Robustness
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('time-behavior')"
          @mouseleave="clearNode"
        >
          <rect
            x="595"
            y="450"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text
            x="660"
            y="475"
            text-anchor="middle"
            class="txt-item"
            @mouseleave="clearNode"
          >
            Time Behavior
          </text>
        </g>

        <line
          x1="820"
          y1="100"
          x2="820"
          y2="120"
          stroke="#333"
          stroke-width="1.5"
        />
        <g
          class="node"
          @mouseenter="setNode('cat-maintenance')"
          @mouseleave="clearNode"
        >
          <rect
            x="740"
            y="120"
            width="160"
            height="50"
            fill="#e1d5e7"
            stroke="#9673a6"
            rx="4"
          />
          <text x="820" y="140" text-anchor="middle" class="txt-cat">
            <tspan x="820" dy="0">Maintenance</tspan>
            <tspan x="820" dy="1.2em">and Evolution</tspan>
          </text>
        </g>
        <path
          d="M 760 170 V 520 M 760 215 h 20 M 760 270 h 20 M 760 320 h 20 M 760 370 h 20 M 760 420 h 20 M 760 470 h 20 M 760 520 h 20"
          stroke="#333"
          fill="none"
        />
        <g
          class="node"
          @mouseenter="setNode('domain-adaptability')"
          @mouseleave="clearNode"
        >
          <rect
            x="780"
            y="190"
            width="130"
            height="50"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="845" y="210" text-anchor="middle" class="txt-item">
            <tspan x="845" dy="0">Domain</tspan>
            <tspan x="845" dy="1.2em">Adaptability</tspan>
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('maintainability')"
          @mouseleave="clearNode"
        >
          <rect
            x="780"
            y="250"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="845" y="275" text-anchor="middle" class="txt-item">
            Maintainability
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('modifiability')"
          @mouseleave="clearNode"
        >
          <rect
            x="780"
            y="300"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="845" y="325" text-anchor="middle" class="txt-item">
            Modifiability
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('portability')"
          @mouseleave="clearNode"
        >
          <rect
            x="780"
            y="350"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="845" y="375" text-anchor="middle" class="txt-item">
            Portability
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('replaceability')"
          @mouseleave="clearNode"
        >
          <rect
            x="780"
            y="400"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="845" y="425" text-anchor="middle" class="txt-item">
            Replaceability
          </text>
        </g>
        <g class="node" @mouseenter="setNode('retrainability')">
          <rect
            x="780"
            y="450"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="845" y="475" text-anchor="middle" class="txt-item">
            Retrainability
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('reusability')"
          @mouseleave="clearNode"
        >
          <rect
            x="780"
            y="500"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="845" y="525" text-anchor="middle" class="txt-item">
            Reusability
          </text>
        </g>

        <line
          x1="1000"
          y1="100"
          x2="1000"
          y2="120"
          stroke="#333"
          stroke-width="1.5"
        />
        <g
          class="node"
          @mouseenter="setNode('cat-responsible')"
          @mouseleave="clearNode"
        >
          <rect
            x="920"
            y="120"
            width="160"
            height="50"
            fill="#e1d5e7"
            stroke="#9673a6"
            rx="4"
          />
          <text x="1000" y="150" text-anchor="middle" class="txt-cat">
            Responsible AI
          </text>
        </g>
        <path
          d="M 940 170 V 500 M 940 210 h 20 M 940 265 h 20 M 940 320 h 20 M 940 375 h 20 M 940 430 h 20 M 940 500 h 20"
          stroke="#333"
          fill="none"
        />
        <g
          class="node"
          @mouseenter="setNode('compliance')"
          @mouseleave="clearNode"
        >
          <rect
            x="960"
            y="190"
            width="140"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="1030" y="215" text-anchor="middle" class="txt-item">
            Compliance
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('economic-risk')"
          @mouseleave="clearNode"
        >
          <rect
            x="960"
            y="240"
            width="140"
            height="50"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="1030" y="260" text-anchor="middle" class="txt-item">
            <tspan x="1030" dy="0">Economic Risk</tspan>
            <tspan x="1030" dy="1.2em">Consideration</tspan>
          </text>
        </g>
        <g class="node" @mouseenter="setNode('fairness')">
          <rect
            x="960"
            y="300"
            width="140"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="1030" y="325" text-anchor="middle" class="txt-item">
            Fairness
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('health-safety')"
          @mouseleave="clearNode"
        >
          <rect
            x="960"
            y="350"
            width="140"
            height="50"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="1030" y="370" text-anchor="middle" class="txt-item">
            <tspan x="1030" dy="0">Health and Safety</tspan>
            <tspan x="1030" dy="1.2em">Risk Consideration</tspan>
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('inclusivity')"
          @mouseleave="clearNode"
        >
          <rect
            x="960"
            y="410"
            width="140"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="1030" y="435" text-anchor="middle" class="txt-item">
            Inclusivity
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('societal-ethical')"
          @mouseleave="clearNode"
        >
          <rect
            x="960"
            y="460"
            width="140"
            height="60"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="1030" y="475" text-anchor="middle" class="txt-item">
            <tspan x="1030" dy="0">Societal</tspan>
            <tspan x="1030" dy="1.2em">and Ethical Risk</tspan>
            <tspan x="1030" dy="1.2em">Consideration</tspan>
          </text>
        </g>

        <line
          x1="1190"
          y1="100"
          x2="1190"
          y2="120"
          stroke="#333"
          stroke-width="1.5"
        />
        <g
          class="node"
          @mouseenter="setNode('cat-security')"
          @mouseleave="clearNode"
        >
          <rect
            x="1110"
            y="120"
            width="160"
            height="50"
            fill="#e1d5e7"
            stroke="#9673a6"
            rx="4"
          />
          <text x="1190" y="140" text-anchor="middle" class="txt-cat">
            <tspan x="1190" dy="0">Security and</tspan>
            <tspan x="1190" dy="1.2em">Privacy</tspan>
          </text>
        </g>
        <path
          d="M 1130 170 V 260 M 1130 210 h 20 M 1130 260 h 20"
          stroke="#333"
          fill="none"
        />
        <g
          class="node"
          @mouseenter="setNode('privacy')"
          @mouseleave="clearNode"
        >
          <rect
            x="1150"
            y="190"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="1215" y="215" text-anchor="middle" class="txt-item">
            Privacy
          </text>
        </g>
        <g
          class="node"
          @mouseenter="setNode('resistance')"
          @mouseleave="clearNode"
        >
          <rect
            x="1150"
            y="240"
            width="130"
            height="40"
            fill="#d5e8d4"
            stroke="#82b366"
          />
          <text x="1215" y="265" text-anchor="middle" class="txt-item">
            Resistance
          </text>
        </g>
      </svg>
    </div>

    <Transition name="slide">
      <div v-if="activeNode" class="description-panel">
        <h4>{{ activeNode.title }}</h4>
        <p>{{ activeNode.description }}</p>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
interface QualityItem {
  title: string;
  description: string;
}

const activeNode = ref<QualityItem | null>(null);

const setNode = (id: string) => {
  if (registry[id]) activeNode.value = registry[id];
};
const clearNode = () => {
  activeNode.value = null;
};

const registry: Dictionary<QualityItem> = {
  "cat-behavior": {
    title: "Behavior Analysis",
    description:
      "QAs related to ease of observing and analyzing ML component behavior at development time and run time.",
  },
  "cat-confidence": {
    title: "Confidence",
    description:
      "QAs related to producing information that increases insight into the model and its outputs",
  },
  "cat-consistency": {
    title: "Consistency",
    description: "QAs related to producing consistent results over time.",
  },
  "cat-operation": {
    title: "Continued Operation",
    description:
      "QAs related to providing continued operation within specified boundaries and constraints.",
  },
  "cat-maintenance": {
    title: "Maintenance and Evolution",
    description:
      "QAs related to ease of maintaining and evolving ML components over time",
  },
  "cat-responsible": {
    title: "Responsible AI",
    description:
      "QAs related to the ethical and societal impact of ML component usage.",
  },
  "cat-security": {
    title: "Security and Privacy",
    description:
      "QAs related to protection and handling of sensitive information",
  },
  analyzability: {
    title: "Analyzability",
    description:
      "Capability of an ML component to expose attributes that enable it to be effectively and efficiently assessed regarding its behavior or the impact of an intended change, to diagnose it for deficiencies or causes of failure, or to identify sub-components to be modified.",
  },
  monitorability: {
    title: "Monitorability",
    description:
      "Capability of an ML component to produce data that can be used to measure runtime attributes (e.g., performance degradation, latency) that can effectively be observed and used by the ML-enabled system or operator to take action aligned with requirements.",
  },
  testability: {
    title: "Testability",
    description:
      "Capability of an ML component to support testing against expected behaviors by offering information relevant to test results or ensuring the visibility of failures.",
  },
  understandability: {
    title: "Understandability",
    description:
      "Ease with which the code, implementation choices, and design choices of an ML component can be understood.",
  },
  explainability: {
    title: "Explainability",
    description:
      "Capability of an ML component to provide information that can explain model outputs (decisions) in human terms.",
  },
  "functional-correctness": {
    title: "Functional Correctness",
    description:
      "Capability of an ML component to meet system-derived correctness or model performance requirements.",
  },
  interpretability: {
    title: "Interpretability",
    description:
      "Capability of an ML component to be transparent in its execution and produce information concerning the relationship between inputs and outputs.",
  },
  repeatability: {
    title: "Repeatability",
    description:
      "Capability of an ML component to produce equivalent results when run on equivalent inputs during inference time.",
  },
  reproducibility: {
    title: "Reproducibility",
    description:
      "Capability of the training algorithm for the ML model to produce functionally-equivalent ML models when run on similar datasets during training time.",
  },
  deployability: {
    title: "Deployability",
    description:
      "Capability of an ML component to be deployed into production when needed, without any unanticipated side effects and within specified resource and time constraints.",
  },
  resilience: {
    title: "Resilience",
    description:
      "Capability of an ML component to provide and maintain an acceptable level of service in the face of technical challenges to normal operation.",
  },
  reliability: {
    title: "Reliability",
    description:
      "Capability of an ML component to perform specified functions without failure under normal operation.",
  },
  "resource-utilization": {
    title: "Resource Utilization",
    description:
      "Capability of an ML component to use no more than the specified amount of resources to perform its function.",
  },
  robustness: {
    title: "Robustness",
    description:
      "Capability of ML component to preserve its level of functional correctness under specified fault modes or conditions.",
  },
  "time-behavior": {
    title: "Time Behavior",
    description:
      "Capability of an ML component to produce outputs within required response time and throughput rates.",
  },
  "domain-adaptability": {
    title: "Domain Adaptability",
    description:
      "Capability of an ML component trained on a source domain to be used in a different, but related domain.",
  },
  maintainability: {
    title: "Maintainability",
    description:
      "Ease with which the ML component can be modified to correct faults, to improve performance or other attributes, or to adapt to a changed environment.",
  },
  modifiability: {
    title: "Modifiability",
    description:
      "Capability of an ML component to be changed without introducing defects, unintended side effects, or degrading existing component quality, and within specified resource and time constraints.",
  },
  portability: {
    title: "Portability",
    description:
      "Capability of an ML component to be adapted for or transferred to different hardware, software, or compute platform, without any unanticipated side effects and within specified resource and time constraints",
  },
  replaceability: {
    title: "Replaceability",
    description:
      "Capability of an ML component to replace (or be replaced by) another ML component for the same purpose in the same environment.",
  },
  retrainability: {
    title: "Retrainability",
    description:
      "Ability to generate a new version of the trained model using the same process on a new set of training data, either manually or automatically depending on system-derived requirements.",
  },
  reusability: {
    title: "Reusability",
    description:
      "Capability of an ML component (or its sub-components) to be used in other ML-enabled systems with minimal change.",
  },
  compliance: {
    title: "Compliance",
    description:
      "Capability of an ML component to satisfy requirements, as required by rules, regulations, laws, standards, or security policies.",
  },
  "economic-risk": {
    title: "Economic Risk Consideration",
    description:
      "Capability of an ML component to mitigate the potential risk of its results to financial status, efficient operation, commercial property, reputation, employment, educational status, or other resources.",
  },
  fairness: {
    title: "Fairness",
    description:
      "Capability of an ML component to produce results that are not biased towards certain populations, including, but not limited to protected attributes (e.g., race, gender, income).",
  },
  "health-safety": {
    title: "Health and Safety Risk Consideration",
    description:
      "Capability of an ML component to mitigate the potential risk of its results to the health and safety of system users.",
  },
  inclusivity: {
    title: "Inclusivity",
    description:
      "Capability of an ML component to be used by systems serving people of various backgrounds, characteristics, or capabilities.",
  },
  "societal-ethical": {
    title: "Societal and Ethical Risk Consideration",
    description:
      "Capability of an ML component to mitigate the potential risk of its results to society.",
  },
  privacy: { title: "Privacy", description: "Data protection and anonymity." },
  resistance: {
    title: "Resistance",
    description: "Defense against adversarial hacking.",
  },
};
</script>

<style scoped>
.model-container {
  position: relative;
  width: 100%;
  height: 100%;
  padding: 20px 0px 0px 0px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.svg-scroll-container {
  width: 100%;
  height: 100%;
  overflow: auto;
  display: flex;
  justify-content: flex-start;
  align-items: flex-start;
}

svg {
  min-width: 900px;
  height: auto;
  display: block;
  margin: 0;
  flex-shrink: 0;
}

.node {
  cursor: pointer;
}

.node:hover rect {
  stroke-width: 3px;
  filter: brightness(0.98);
}

text {
  font-family: "Segoe UI", Tahoma, Geneva, Verdana, sans-serif;
  pointer-events: none;
  fill: #333;
}

.txt-root {
  font-weight: 800;
  font-size: 28px; /* Heavily increased for the main header */
  fill: #000;
}

.txt-cat {
  font-weight: 700;
  font-size: 20px; /* Equivalent to a sub-header */
}

.txt-item {
  font-size: 17px; /* This will now feel like standard 16px-18px page text */
  font-weight: 500;
}

.description-panel {
  position: absolute;
  bottom: 30px;
  right: 30px;
  width: 320px;
  padding: 1.5rem;
  background: #ffffff;
  border-left: 5px solid #9673a6;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
  border-radius: 4px;
}

.description-panel h4 {
  margin: 0 0 10px 0;
  font-size: 1.1rem;
  color: #1a1a1a;
}
.description-panel p {
  margin: 0;
  font-size: 0.95rem;
  color: #555;
  line-height: 1.4;
}

/* Transitions */
.slide-enter-active,
.slide-leave-active {
  transition: all 0.3s ease;
}
.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
</style>
