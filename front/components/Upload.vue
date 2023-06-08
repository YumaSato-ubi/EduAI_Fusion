<template>
    <div>
        <h2 v-if="!result">画像をアップロードしてください</h2>
        <!-- <h2 v-if="result">{{ result }}</h2> -->
        <img :src="result" />
        <label v-if="!value" class="upload-content-space user-photo default">
            <input class="file-button" type="file" @change="upload" />
            アップロード
        </label>
        <div v-if="value" class="uploaded">
            <label class="upload-content-space user-photo">
                <input class="file-button" type="file" @change="upload" />
                <img class="user-photo-image" :src="value" />
                <button class="judge-button" @click="judge">判定</button>
            </label> 
        </div>
    </div>
</template>

<script>
export default {
    name: 'Upload',
    props: {
        value: {
            type: String,
            default: null
        }
    },
    data() {
        return {
            file: null,
            picture: '',
            result: '',
            sentence: ''
        }
    },
    methods: {
        async upload(event) {
            const files = event.target.files || event.dataTransfer.files
            const file = files[0]

            if (this.checkFile(file)) {
                this.picture = await this.getBase64(file)
                this.$emit('input', this.picture)
            }
        },
        getBase64(file) {
            return new Promise((resolve, reject) => {
                const reader = new FileReader()
                reader.readAsDataURL(file)
                reader.onload = () => resolve(reader.result)
                reader.onerror = error => reject(error)
            })
        },
        checkFile(file) {
            let result = true
            if (!file) {
                result = false
            }
            if (file.type !== 'image/jpeg' && file.type !== 'image/png') {
                result = false
            }
            return result
        },
        async judge() {
          var params = new FormData()
          params.append('image', this.picture)
          const res = await this.$axios.$post('http://127.0.0.1:5000/', params, {withCredentials: true})
          this.result = "data:image/png;base64," + res;
          console.log(this.result)
        }

    }
}
</script>

<style scoped>
span {
  color: #e2162e;
  font-size: 60px;
}
.user-photo {
  cursor: pointer;
  outline: none;
  justify-content: center;
}

.user-photo.default {
  align-items: center;
  background-color: #0074fb;
  border: 1px solid #0051b0;
  border-radius: 2px;
  box-sizing: border-box;
  display: inline-flex;
  font-weight: 600;
  justify-content: center;
  letter-spacing: 0.3px;
  color: #fff;
  height: 4rem;
  padding: 0 1.6rem;
  max-width: 177px;
}

.user-photo.default:hover {
  background-color: #4c9dfc;
}

.user-photo.default:active {
  background-color: #0051b0;
}

.user-photo-image {
  max-width: 300px;
  display: block;
}

.user-photo-image:hover {
  opacity: 0.8;
}

.file-button {
  display: none;
}

.uploaded {
  display: flex;
  justify-content: center;
}

.judge-button {
  align-items: center;
  background-color: #0074fb;
  border: 1px solid #0051b0;
  border-radius: 2px;
  box-sizing: border-box;
  display: inline-flex;
  font-weight: 600;
  justify-content: center;
  letter-spacing: 0.3px;
  color: #fff;
  height: 4rem;
  padding: 0 1.6rem;
  margin-top: 2rem;
  width: 300px;
  cursor: pointer;
  outline: none;
}

</style>