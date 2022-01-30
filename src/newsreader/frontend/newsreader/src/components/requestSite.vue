<template>
<div>
  <input type="text" v-model="payload.site_url" @keyup.enter="getData(payload)">
  <br>
  <br>
  <br>
  <br>
  <div v-if="loading_state">
    <h1>Loading....<span class="animate_load_state"></span></h1>
  </div>
  <h1 v-if="recieved_html_response">Error Recived: {{recieved_html_response}}</h1>
</div>
</template>


<script setup lang="ts">
import { ref, reactive } from 'vue'
import axios, { AxiosRequestConfig, AxiosResponse } from 'axios'
axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'HTTP_X_CSRFTOKEN'

const payload = reactive({
    site_url: '',
})

let recieved_html_response = ref('')
let loading_state= ref(false)

const cookie = document.cookie
const optionalHeaders = {'X-CSRFToken':'',
'content-type':'',}

const cookieSearchTerm = cookie.indexOf('csrftoken=')
const CSRF_TOKEN = cookie.substring(cookieSearchTerm).split('csrftoken=')[1]

if (cookieSearchTerm >= 0){
  optionalHeaders['X-CSRFToken'] = `${CSRF_TOKEN}`
  optionalHeaders['content-type'] = 'application/json'
} else {
  throw new Error("Token not established")
}

const sitePOSTconfig: AxiosRequestConfig = {
    baseURL: 'http://localhost:80/projects/newsreader',
    url: '/submit-url',
    method: 'post',
    headers: {...optionalHeaders},  
    xsrfCookieName: 'csrftoken',
    xsrfHeaderName: 'HTTP_X_CSRFTOKEN',
    timeout: 1500,
    
}

async function getData(payload: any){
  loading_state.value = true
  const dataResponse = await axios.post('http://localhost:80/projects/newsreader/submit-url', payload, sitePOSTconfig)
  .catch((err) => {recieved_html_response.value = err})
}




</script>


<style scoped>
a {
  color: #42b983;
}

label {
  margin: 0 0.5em;
  font-weight: bold;
}

code {
  background-color: #eee;
  padding: 2px 4px;
  border-radius: 4px;
  color: #304455;
}
.animate_load_state::before {
  position: absolute;
  content: "⌛";
  opacity: 0;
  animation: 750ms clock_animation_show 100ms ease-in-out alternate infinite;
}

@keyframes clock_animation_show {
  100% {
    opacity: 1;
  }
}
</style>
