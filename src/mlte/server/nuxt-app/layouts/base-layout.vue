<template>
  <div>
    <div style="height: 16px; background-color: #f3ca3e;"/>
    <header>
      MLTE Machine Learning Test and Evaluation
    </header>

    <div class="body-div">
      <slot name="default"/>
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
        <a>Version</a>
      </div>
    </footer>
  </div>
</template>

<style>
  header {
    margin-bottom: 8px;
    padding: 25px;
    font-size: 48px;
    color: white;
    background-color: #2d2f30;
  }

  .body-div {
    margin-top: 8px;
    padding-left: 40px;
    padding-right: 40px;
    max-width: 100ch;
    margin-left: auto;
    margin-right: auto;
  }

  footer {
    margin-top: 8px;
    bottom: 0;
    left: 0;
    width: 100%;
    height: 90px;
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

  footer > div > a {
    padding-left: 30px;
  }
</style>