<template>
    <div class="accordion">
      <div class="accordion-item">
        <div class="accordion-item-header">
          
            Explainability
          <input type="checkbox" id="formCompleted" disabled />
          <div class="accordion-item-header-content">
           
          </div>
        </div>
        <div class="accordion-item-body">
          <div class="accordion-item-body-content">
            <form @input="checkFormCompletion">
  
              <div class="form-group">
                <p>Explainability is the ability to explain the output of the flower classification model deployed in a handheld flower identification device. Different technical and non-technical stakeholders might 
                  have different expectations of explainability methods which is why 
                  it might be helpful to discuss this with them to help you choose the most suitable techniques. </p>
                  
                <label for="stakeholders">Stakeholders</label>
                <select id="stakeholders" name="stakeholders">
                  <option value="endUser">Behavioral ecologists</option>
                  <option value="businessAnalyst"></option>
                  <option value="complianceOfficer">Plant enthusiasts</option>
                  <option value="developer">Regulatory agencies</option>
                  <option value="developer">Data Scientists</option>
                  <option value="custom">Other</option>
                </select>
                <input type="text" id="customStakeholder" name="customStakeholder" placeholder="Enter custom stakeholder" style="display: none;" />
              </div>
  
              <div class="form-group">
                <label for="stimulus">What specific events or actions might trigger the need for an explanation?              </label>
                <label for="stimulus"> Stimulus</label>
                <input type="text" id="stimulus" name="stimulus" placeholder="Behavioral ecologist requests explanation for prediction" />
              </div>
  
              <div class="form-group">
                <label for="stimulusSource">Who needs the explanations?</label>
                <label for="stimulusSource">Source</label>
                <input type="text" id="stimulusSource" name="stimulusSource" placeholder="Internal system log" />
              </div>
  
              <div class="form-group">
                <label for="environment">Are there any specific contexts or situations that impact the explanation requirements?</label>
                <label for="environment">Environment</label>
                <input type="text" id="environment" name="environment" placeholder="During peak usage hours" />
              </div>
  
              <div class="form-group">
                <label for="response">What type of explanation or information should be provided?
                </label>
                <label for="response">Response</label>
                <input type="text" id="response" name="response" placeholder="Explanations for individual predictions" />
              </div>
  
              <div class="form-group">
                <label for="responseMeasure"> How will you measure if the explanation meets the needs of the stakeholder?              </label>
                <label for="responseMeasure">Response Measure</label>
                <input type="text" id="responseMeasure" name="responseMeasure" placeholder="Meet with stakeholder, more than one technique" />
              </div>
  
              <div class="form-group">
                <label for="explainabilityGoals">Other Explainability Goals in product development</label>
                <input type="text" id="explainabilityGoals" name="explainabilityGoals" placeholder="Include explainability during marketing" />
              </div>
           
  
              <div class="form-group">
                <label for="challenges">Challenges and Constraints</label>
                <h4> accuracy vs interpretability</h4>
                <p>consider the tradeoff between accuracy and interpretability in relation to the expectations of stakeholders, ethical implications and business objectives.</p>
              </div>
            
  
              <button type="button" @click="saveForm" class="save-button">Save</button>
            </form>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import { ref, onMounted } from 'vue';
  
  export default {
    name: 'Accordion',
    setup() {
      const formCompleted = ref(false);
  
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
  
        // Show/hide custom input fields based on selection
        const stakeholderSelect = document.getElementById('stakeholders');
        const customStakeholderInput = document.getElementById('customStakeholder');
        stakeholderSelect.addEventListener('change', () => {
          customStakeholderInput.style.display = stakeholderSelect.value === 'custom' ? 'block' : 'none';
        });
  
        const toolsSelect = document.getElementById('tools');
        const customToolInput = document.getElementById('customTool');
        toolsSelect.addEventListener('change', () => {
          customToolInput.style.display = toolsSelect.value === 'custom' ? 'block' : 'none';
        });
      });
  
      const checkFormCompletion = () => {
        const form = document.querySelector('form');
        const inputs = form.querySelectorAll('input[type="text"], select');
        const allFilled = Array.from(inputs).every(input => input.value.trim() !== '' || (input.style.display === 'none'));
        formCompleted.value = allFilled;
        document.getElementById('formCompleted').checked = allFilled;
      };
  
      const saveForm = () => {
        alert('Form has been saved!');
      };
  
      return {
        formCompleted,
        checkFormCompletion,
        saveForm,
      };
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
  
  .accordion-item-header input[type="checkbox"] {
    margin-right: 1rem;
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
  
  .form-group {
    margin-bottom: 1rem;
  }
  
  label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
  }
  
  input, select {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ccc;
    border-radius: 0.25rem;
  }
  
  input[type="text"] {
    height: 2rem;
  }
  
  select {
    height: 2.5rem;
  }
  
  input::placeholder {
    color: #888;
  }
  
  .save-button {
    margin-top: 1rem;
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 0.25rem;
    background-color: #007bff;
    color: white;
    font-size: 1rem;
    cursor: pointer;
  }
  
  .save-button:hover {
    background-color: #0056b3;
  }
  </style>
  