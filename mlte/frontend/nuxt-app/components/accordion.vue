<template>
  <div>
    <div class="accordion-item">
      <div class="accordion-item-header" @click="toggleAccordion">
        <span :class="{'rotate-symbol': isOpen}">▼</span>
        <span class="circle top-priority"></span>
        <h2>{{ title }}</h2>
      </div>
      <div :class="['accordion-item-body', { 'accordion-item-open': isOpen }]" ref="accordionItemBody">
        <slot name="content"></slot>
      </div>
    </div>
  </div> 
</template>

<script>
import { defineComponent, ref } from 'vue';

export default defineComponent({
  name: 'Accordion',
  props: {
    title: {
      type: String,
      required: true,
    },
  },
  setup() {
    const accordionItemBody = ref(null);
    const isOpen = ref(false);

    const toggleAccordion = () => {
      if (accordionItemBody.value) {
        if (accordionItemBody.value.style.maxHeight) {
          accordionItemBody.value.style.maxHeight = null;
          isOpen.value = false;
        } else {
          accordionItemBody.value.style.maxHeight = `${accordionItemBody.value.scrollHeight}px`;
          isOpen.value = true;
        }
      }
    };

    return {
      accordionItemBody,
      toggleAccordion,
      isOpen,
    };
  },
});
</script>

<style scoped>
.accordion-item-header {
  display: flex;
  align-items: center;
  cursor: pointer;
  background-color: #eee;
  padding: 1.5rem;
  border: 1px solid #ccc;
  border-radius: 5px;
  margin-bottom: 5px;
}

.accordion-item-header span {
  display: inline-block;
  margin-right: 10px;
  transition: transform 0.2s;
}

.rotate-symbol {
  transform: rotate(180deg);
}

.accordion {
    background-color: whitesmoke;
    color: #444;
    cursor: pointer;
    padding: 18px;
    width: 100%;
    text-align: left;
    border: none;
    outline: none;
    transition: 0.4s;
  }
  
.accordion{
  width: 90%; 
  max-width: 1000px;
  margin: 0rem auto;
}



 .accordion-item-header{
  padding: 0.5rem 3rem 0.5rem 1rem;
  min-height: 3.5rem;
  line-height: 1.25rem;
  font-weight: bold;
  display: flex;
  align-items: center;
  position: relative;
  cursor: pointer;
  }

  .accordion-item-header-content{
    margin-left: auto;
    padding-left: 1rem;
    font-size: 15px;
  }

.accordion-item-body{
  max-height: 0; 
  overflow: hidden;
  transition: max-height 0.2s ease-out;

}

.accordion-item-open{
  background-color: #f8f8f8;
  border: 1px solid #ccc;
  padding: 1rem;  
  margin-top: -1px; 
  max-height: 300px; 
  overflow-y: auto; 
}

.circle{
    height: 15px;
      width: 15px;
      border-radius: 50%;
      display: inline-block;
}
.top-priority {
    background-color: #d01818;
  }

</style>
