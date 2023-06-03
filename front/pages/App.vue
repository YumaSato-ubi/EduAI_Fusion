<template>
    <div class="background">
      <h1>EduAI Fusion</h1>
      <Upload v-model="picture" />
      <!-- <img :src="picture" /> -->
    </div>
  </template>
  
  <script>
  import Upload from '../components/Upload.vue';
  
  export default {
    name: 'app',
    components: {
        Upload
    },
    data(){
      return {
        picture: null
      };
    }
  }
  </script>

<style>
* {
    box-sizing: border-box;
}
html {
    font-size: 62.5%
}
body {
    color: #2c2d30;
    font-size: 1.6rem;
    font-family: "Hiragino Kaku Gothic Pro", "ヒラギノ角ゴ Pro W3", "Meiryo",
    "メイリオ", "Osaka", "MS PGothic", arial, helvetica, clean, sans-serif;
    line-height: 1.5;
    background-image: url("EduAI_logo.PNG");
    background-size: contain;
    background-color:rgba(255,255,255,0.9);
    background-blend-mode:lighten;
};
</style>