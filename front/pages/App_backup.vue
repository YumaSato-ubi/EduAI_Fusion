<template>
    <div style="text-align: center">
      <h1>画像判定</h1>
      <h2>画像をアップロードしてください</h2>
      <div 
      class="image-input__field"
      :class="{ over: isDragOver }"
      @dragover.prevent="onDrag('over')"
      @dragleave="onDrag('leave')"
      @drop.stop="onDrop"
      >
        <p>画像をドラッグ&ドロップ</p>
      </div>
      <!-- <img :src="image.src" /> -->
      <NuxtLink to='/result'>判定</NuxtLink>
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
        isDragOver: false
      };
    },
    methods: {
      onDrag(type){
        this.isDragOver = type === "over"
      },
      onDrop(event){
        this.isDragOver = false;
        const files = event.dataTransfer.files;
        if (files.length != 1) {
          return;
        }
        this.readImage(files[0]);
      },
      readImage(file) {
        let reader = new FileReader();
        reader.onload = this.loadImage;
        reader.readAsDataURL(file);
      },
      loadImage(e){
        let image = new Image();
        image.src = e.target.result;
        this.image = image;
      }
    }
  }
  </script>