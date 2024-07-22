<template>
    <div class="accordion">
      <div class="accordion-item">
        <div class="accordion-item-header">
          Explainability
          <div class="accordion-item-header-content">
            Fall 2024
          </div>
        </div>
        <div class="accordion-item-body">
          <div class="accordion-item-body-content">
            Content
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { onMounted } from 'vue';
  
  export default {
    name: 'Accordion',
    setup() {
      onMounted(() => {
        const accordionItemHeaders = document.querySelectorAll('.accordion-item-header');
  
        accordionItemHeaders.forEach(accordionItemHeader => {
          accordionItemHeader.addEventListener('click', event => {
            accordionItemHeader.classList.toggle('active');
            const accordionItemBody = accordionItemHeader.nextElementSibling;
            if (accordionItemHeader.classList.contains('active')) {
              accordionItemBody.style.maxHeight = accordionItemBody.scrollHeight + 'px';
            } else {
              accordionItemBody.style.maxHeight = 0;
            }
          });
        });
      });
    },
  };
  </script>
  
  <style scoped>
  .accordion {
    width: 90%;
    max-width: 1000px;
    margin: 0.5rem auto;
  }
  
  .accordion-item {
    color: black;
    margin: 0.3rem 0;
    border-radius: 0.5rem;
  }
  
  .accordion-item-header {
    padding: 0.5rem 3rem 0.5rem 1rem;
    min-height: 3.5rem;
    line-height: 1.25rem;
    font-weight: bold;
    display: flex;
    align-items: center;
    position: relative;
    cursor: pointer;
  }
  
  .accordion-item-header-content {
    margin-left: auto;
    padding-left: 1rem;
    font-size: 15px;
  }
  
  .accordion-item-header::after {
    content: ">";
    font-size: 2rem;
    position: absolute;
    left: -10px;
    transition: transform 0.2s ease-in-out;
  }
  
  .accordion-item-header.active::after {
    transform: rotate(90deg);
  }
  
  .accordion-item-body {
    max-height: 0;
    overflow: hidden;
    transition: max-height 0.2s ease-out;
  }
  
  .accordion-item-body-content {
    padding: 1rem;
    line-height: 1.5rem;
  }
  </style>
  