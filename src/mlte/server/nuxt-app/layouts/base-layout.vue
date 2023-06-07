<template>
  <div>
    <div style="height: 16px; background-color: #f3ca3e;"/>
    <header class="flex-container">
      <div class="header-main">
        MLTE
      </div>
      <div class="header-secondary">
        Machine Learning <br/>
        Test and Evaluation
      </div>
    </header>

    <div class="flex-container">
      <div class="sidebar">
        <slot name="sidebar"/>
      </div>

      <div class="body-div">
        <slot name="default"/>
      </div>
    </div>

    <footer>
      <p class="footer-text-left">
        <b>MLTE - 2023</b>
      </p>
      <div class="footer-text-right">
        <a target="_blank" rel="noopener noreferrer" href="https://github.com/mlte-team">Github</a>
        <a>Docs</a>
        <a>User Guide</a>
        <a>Keep in Touch</a>
        <span>Version</span>
      </div>
    </footer>
  </div>
</template>


<style>
  header {
    margin-bottom: 8px;
    padding: 25px;
    color: white;
    background-color: #2d2f30;
  }

  .header-main {
    font-size: 56px;
    margin-right: 8px;
  }

  .header-secondary {
    font-size: 24px;
    padding-top: 5px;
  }

  .flex-container {
    display: flex;
  }

  .sidebar {
    width: 100%;
    max-width: 30ch;
    margin-left: 40px;
  }

  .body-div {
    width: 100%;
    max-width: 100ch;
    margin-top: 8px;
    margin-left: 40px;
    padding-right: 40px;
  }

  footer {
    width: 100%;
    height: 90px;
    margin-top: 8px;
    bottom: 0;
    left: 0;
    font-size: 16px;
  }

  .footer-text-left {
    padding-left: 40px;
    float: left;
  }

  .footer-text-right {
    padding-right: 40px;
    margin-top: 20px;
    float: right;
  }

  footer > div > a,
  footer > div > span {
    padding-left: 30px;
  }
</style>